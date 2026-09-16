"""Resolver + dataflow V2: sparse worklist, candidate sets và evidence paths."""

from __future__ import annotations

import time
import hashlib
from collections import defaultdict, deque
from dataclasses import dataclass

from l3gen.core.semantics.registry import SemanticRegistry, builtin_registry
from l3gen.models.resolution import (
    AbstractValue,
    EvidenceStep,
    ResolvedCall,
    ResolutionMetrics,
    ResolutionResult,
)
from l3gen.models.semantic import (
    AssignmentFact,
    CallFact,
    DefinitionFact,
    ExpressionIR,
    ImportFact,
    InheritanceFact,
    ParameterFact,
    ReturnFact,
    ScopeFact,
    SemanticFact,
    SemanticProgram,
)

MAX_CANDIDATES_PER_CALL = 32
MAX_VALUES_PER_SLOT = 128
MAX_PROPAGATIONS = 250_000
MAX_EVIDENCE_STEPS = 12


@dataclass(frozen=True)
class _Edge:
    target: str
    evidence: EvidenceStep


@dataclass(frozen=True)
class _Binding:
    slot: str
    fact: SemanticFact
    conditional: bool = False


class DataflowResolver:
    def __init__(
        self,
        program: SemanticProgram,
        registry: SemanticRegistry | None = None,
        max_candidates: int = MAX_CANDIDATES_PER_CALL,
        max_propagations: int = MAX_PROPAGATIONS,
    ) -> None:
        self.program = program
        self.registry = registry or builtin_registry()
        self.max_candidates = max_candidates
        self.max_propagations = max_propagations
        if max_candidates < 1 or max_propagations < 1:
            raise ValueError("giới hạn candidate và propagation phải lớn hơn 0")
        self.facts = program.all_facts()
        self.scopes = {fact.scope_id: fact for fact in self.facts if isinstance(fact, ScopeFact)}
        self.parent_scope = {
            fact.scope_id: fact.parent_scope_id for fact in self.facts if isinstance(fact, ScopeFact)
        }
        self.definitions = {
            fact.qualified_name: fact for fact in self.facts if isinstance(fact, DefinitionFact)
        }
        self.definition_by_scope_name: dict[tuple[str, str], list[DefinitionFact]] = defaultdict(list)
        self.import_by_scope_name: dict[tuple[str, str], list[ImportFact]] = defaultdict(list)
        self.local_names: dict[str, set[str]] = defaultdict(set)
        self.bindings: dict[tuple[str, str], list[_Binding]] = defaultdict(list)
        self.binding_slot_by_fact: dict[str, str] = {}
        self.parameters: dict[str, list[ParameterFact]] = defaultdict(list)
        self.returns: dict[str, list[ReturnFact]] = defaultdict(list)
        self.module_by_scope: dict[str, str] = {}
        self.global_slots: dict[str, list[str]] = {}
        self.internal_bases: dict[str, list[str]] = defaultdict(list)
        self.mro_cache: dict[str, list[str] | None] = {}
        self.values: dict[str, dict[str, AbstractValue]] = defaultdict(dict)
        self.evidence: dict[tuple[str, str], list[EvidenceStep]] = {}
        self.edges: dict[str, list[_Edge]] = defaultdict(list)
        self.edge_keys: set[tuple[str, str]] = set()
        self.queue: deque[tuple[str, str]] = deque()
        self.call_watchers: dict[str, list[CallFact]] = defaultdict(list)
        self.receiver_watchers: dict[str, set[str]] = defaultdict(set)
        self.attr_reads: dict[str, list[tuple[str, str, SemanticFact]]] = defaultdict(list)
        self.attr_writes: dict[str, list[tuple[str, str, SemanticFact]]] = defaultdict(list)
        self.call_targets: dict[str, set[str]] = defaultdict(set)
        self.call_receiver_types: dict[str, set[str]] = defaultdict(set)
        self.call_runtime: dict[str, list[EvidenceStep]] = defaultdict(list)
        self.call_truncated: set[str] = set()
        self.truncated_slots: set[str] = set()
        self.worklist_cutoff = False
        self.calls = {fact.id: fact for fact in self.facts if isinstance(fact, CallFact)}
        self.callee_slots: dict[str, str] = {}
        self.receiver_slots: dict[str, str] = {}
        self.argument_slots: dict[str, list[str]] = defaultdict(list)
        self.keyword_slots: dict[str, dict[str, str]] = defaultdict(dict)
        self.call_by_signature: dict[tuple[str, str, int, str], list[CallFact]] = defaultdict(list)
        self.call_by_location_text: dict[tuple[str, int, str], list[CallFact]] = defaultdict(list)
        self.calls_at_position = {
            (call.location.file, call.location.line_start, call.location.column_start): call
            for call in self.calls.values()
        }
        self.known_modules = {
            ".".join(module.module.split(".")[:end])
            for module in program.modules
            for end in range(1, len(module.module.split(".")) + 1)
        }
        self.expression_cache: dict[tuple[str, str, str], str] = {}
        self.base_slots: dict[str, list[str]] = defaultdict(list)
        self.metrics = ResolutionMetrics()
        self.partial_reasons: list[str] = []
        self._index()

    def _index(self) -> None:
        for fact in self.facts:
            if isinstance(fact, ScopeFact) and fact.scope_kind == "module":
                self.module_by_scope[fact.scope_id] = fact.qualified_name
        for fact in self.facts:
            if isinstance(fact, ImportFact):
                self.import_by_scope_name[(fact.scope_id, fact.local_name)].append(fact)
                self._register_binding(fact, fact.local_name)
            elif isinstance(fact, DefinitionFact):
                self.definition_by_scope_name[(fact.scope_id, fact.name)].append(fact)
                self._register_binding(fact, fact.name, bool(fact.conditions))
            elif isinstance(fact, ParameterFact):
                self.parameters[fact.function_symbol].append(fact)
                self._register_binding(fact, fact.name)
            elif isinstance(fact, AssignmentFact) and fact.target.kind == "name":
                name = fact.target.name or fact.target.text
                self._register_binding(fact, name, bool(fact.conditions))
            elif isinstance(fact, ReturnFact):
                self.returns[fact.function_symbol].append(fact)
            elif isinstance(fact, CallFact):
                key = (fact.scope_id, fact.location.file, fact.location.line_start, fact.expression_text)
                self.call_by_signature[key].append(fact)
                self.call_by_location_text[
                    (fact.location.file, fact.location.line_start, fact.expression_text)
                ].append(fact)
        for values in self.parameters.values():
            values.sort(key=lambda item: (item.position < 0, item.position, item.name))
        for (scope_id, name), bindings in self.bindings.items():
            bindings.sort(key=lambda item: self._location_key(item.fact))
            if scope_id in self.module_by_scope:
                module = self.module_by_scope[scope_id]
                self.global_slots[f"{module}.{name}"] = self._reaching(bindings)
        self.metrics.symbols = len(self.definitions)

    def _register_binding(
        self, fact: SemanticFact, name: str, conditional: bool = False
    ) -> None:
        self.local_names[fact.scope_id].add(name)
        slot = f"binding:{fact.scope_id}:{name}:{fact.id}"
        self.binding_slot_by_fact[fact.id] = slot
        self.bindings[(fact.scope_id, name)].append(_Binding(slot, fact, conditional))

    def run(self) -> ResolutionResult:
        started = time.perf_counter()
        self._seed_bindings()
        self._build_class_bases()
        self._build_constraints()
        self._run_worklist()
        self._propagate_truncation()
        calls = self._finalize_calls()
        self.metrics.duration_seconds = round(time.perf_counter() - started, 6)
        return ResolutionResult(
            calls=calls,
            values_by_slot={
                slot: sorted(items.values(), key=lambda value: value.key)
                for slot, items in sorted(self.values.items())
                if items
            },
            metrics=self.metrics,
            partial=bool(self.partial_reasons),
            partial_reasons=list(dict.fromkeys(self.partial_reasons)),
            class_bases={
                symbol: sorted({value.value for slot in slots for value in self.values.get(slot, {}).values() if value.kind == "symbol"})
                for symbol, slots in self.base_slots.items()
            },
        )

    def _seed_bindings(self) -> None:
        for fact in self.facts:
            if isinstance(fact, ImportFact) and not fact.is_wildcard:
                local_slot = self.binding_slot_by_fact[fact.id]
                imported_slots = self.global_slots.get(fact.imported_symbol, [])
                if imported_slots:
                    for imported_slot in imported_slots:
                        self._add_edge(
                            imported_slot,
                            local_slot,
                            self._step(fact, f"import giá trị {fact.imported_symbol}"),
                        )
                    continue
                kind = "class" if fact.imported_symbol in self.registry.types else "external"
                self._add_value(
                    local_slot,
                    AbstractValue(kind="symbol", value=fact.imported_symbol, symbol_kind=kind),
                    self._step(fact, f"import {fact.local_name} từ {fact.imported_symbol}"),
                )
            elif isinstance(fact, DefinitionFact):
                kind = "class" if fact.symbol_kind == "class" else "function"
                self._add_value(
                    self.binding_slot_by_fact[fact.id],
                    AbstractValue(kind="symbol", value=fact.qualified_name, symbol_kind=kind),
                    self._step(fact, f"định nghĩa {fact.qualified_name}"),
                )
                if fact.return_annotation is not None and not self.returns.get(fact.qualified_name):
                    type_symbol = self._resolve_type_annotation(fact.scope_id, fact.return_annotation)
                    if type_symbol:
                        self._add_value(self._return(fact.qualified_name),
                            AbstractValue(kind="instance", value=f"return-annotation:{fact.id}", type_symbol=type_symbol),
                            self._step(fact, "kiểu trả về khai trong annotation/stub"))
            elif isinstance(fact, ParameterFact) and fact.annotation is not None:
                type_symbol = self._resolve_type_annotation(fact.scope_id, fact.annotation)
                if type_symbol:
                    self._add_value(
                        self.binding_slot_by_fact[fact.id],
                        AbstractValue(
                            kind="instance",
                            value=f"annotation:{fact.id}",
                            type_symbol=type_symbol,
                        ),
                        self._step(fact, f"annotation của {fact.name} là {type_symbol}"),
                    )

    def _build_class_bases(self) -> None:
        for fact in self.facts:
            if not isinstance(fact, InheritanceFact):
                continue
            for base in fact.bases:
                symbol = self._static_symbol(fact.scope_id, base)
                if symbol:
                    self.internal_bases[fact.class_symbol].append(symbol)

    def _build_constraints(self) -> None:
        for fact in self.facts:
            if isinstance(fact, InheritanceFact):
                self.base_slots[fact.class_symbol] = [
                    self._expression_slot(base, fact, f"base:{index}")
                    for index, base in enumerate(fact.bases)
                ]
            if isinstance(fact, AssignmentFact):
                source = self._expression_slot(fact.value, fact, "value") if fact.has_value else None
                if fact.target.kind == "name":
                    target = self.binding_slot_by_fact[fact.id]
                    if source is not None:
                        self._add_edge(source, target, self._step(fact, f"gán {fact.value.text} vào {fact.target.text}"))
                    if fact.annotation:
                        type_symbol = self._resolve_type_annotation(fact.scope_id, fact.annotation)
                        if type_symbol:
                            self._add_value(
                                target,
                                AbstractValue(
                                    kind="instance",
                                    value=f"annotation:{fact.id}",
                                    type_symbol=type_symbol,
                                ),
                                self._step(fact, f"annotation của {fact.target.text} là {type_symbol}"),
                            )
                elif fact.target.kind == "attribute" and fact.target.base is not None and source is not None:
                    receiver = self._expression_slot(fact.target.base, fact, "assign_receiver")
                    self.attr_writes[receiver].append((fact.target.attribute or "?", source, fact))
            elif isinstance(fact, ReturnFact) and fact.value is not None:
                source = self._expression_slot(fact.value, fact, "return_value")
                self._add_edge(
                    source,
                    self._return(fact.function_symbol),
                    self._step(fact, f"trả {fact.value.text} từ {fact.function_symbol}"),
                )
            elif isinstance(fact, ParameterFact) and fact.default is not None:
                source = self._expression_slot(fact.default, fact, "default")
                self._add_edge(
                    source,
                    self.binding_slot_by_fact[fact.id],
                    self._step(fact, f"giá trị mặc định truyền vào parameter {fact.name}"),
                )

        for call in self.calls.values():
            callee_slot = self._expression_slot(call.callee, call, "callee")
            self.callee_slots[call.id] = callee_slot
            self.call_watchers[callee_slot].append(call)
            if call.callee.kind == "attribute" and call.callee.base is not None:
                receiver = self._expression_slot(call.callee.base, call, "callee:base")
                self.receiver_slots[call.id] = receiver
                self.receiver_watchers[receiver].add(call.id)
                for value in self.values.get(receiver, {}).values():
                    self._record_receiver_type(call.id, value)
            for index, argument in enumerate(call.arguments):
                self.argument_slots[call.id].append(
                    self._expression_slot(argument, call, f"argument:{index}")
                )
            for name, expression in call.keywords.items():
                self.keyword_slots[call.id][name] = self._expression_slot(
                    expression, call, f"keyword:{name}"
                )
            for key in list(self.values.get(callee_slot, {})):
                self._handle_call_value(call, self.values[callee_slot][key], callee_slot)

    def _expression_slot(self, expr: ExpressionIR, fact: SemanticFact, role: str) -> str:
        key = (fact.id, role, expr.text)
        if key not in self.expression_cache:
            self.expression_cache[key] = self._build_expression_slot(expr, fact, role)
        return self.expression_cache[key]

    def _build_expression_slot(self, expr: ExpressionIR, fact: SemanticFact, role: str) -> str:
        if expr.kind == "name":
            name = expr.name or expr.text
            slots = self._lookup_vars(fact.scope_id, name, fact)
            if len(slots) == 1:
                return slots[0]
            if slots:
                target = self._expr(fact.id, role, expr.text)
                for source in slots:
                    self._add_edge(
                        source,
                        target,
                        self._step(fact, f"{name} có nhiều binding có thể tới được"),
                    )
                return target
            builtin = f"builtins.{name}"
            slot = self._expr(fact.id, role, expr.text)
            if builtin in self.registry.callables and name not in self.local_names.get(fact.scope_id, set()):
                self._add_value(
                    slot,
                    AbstractValue(kind="symbol", value=builtin, symbol_kind="function"),
                    self._step(fact, f"{name} là builtin {builtin}"),
                )
            else:
                self._add_value(
                    slot,
                    AbstractValue(kind="unknown", value=name),
                    self._step(fact, f"không tìm thấy binding của {name}"),
                )
            return slot
        if expr.kind == "literal":
            slot = self._expr(fact.id, role, expr.text)
            self._add_value(
                slot,
                AbstractValue(kind="literal", value=expr.text),
                self._step(fact, f"literal {expr.text}"),
            )
            return slot
        if expr.kind in ("list", "tuple"):
            slot = self._expr(fact.id, role, expr.text)
            self._add_value(slot, AbstractValue(kind="container", value=slot), self._step(fact, "container tĩnh"))
            for index, element in enumerate(expr.elements):
                source = self._expression_slot(element, fact, f"{role}:item:{index}")
                self._add_edge(source, f"items:{slot}", self._step(fact, f"phần tử {index} của container"))
            return slot
        if expr.kind == "call":
            call = self.calls_at_position.get(
                (fact.location.file, expr.source_line, expr.source_column)
            ) if expr.source_line is not None else self._find_call(fact, expr.text)
            if call is not None:
                return self._call_result(call.id)
        if expr.kind == "attribute" and expr.base is not None:
            receiver = self._expression_slot(expr.base, fact, f"{role}:base")
            target = self._expr(fact.id, role, expr.text)
            self.attr_reads[receiver].append((expr.attribute or "?", target, fact))
            for value in self.values.get(receiver, {}).values():
                self._handle_attribute_read(value, expr.attribute or "?", target, fact, receiver)
            return target
        if expr.kind == "conditional" and len(expr.elements) >= 3:
            target = self._expr(fact.id, role, expr.text)
            for index, branch in enumerate(expr.elements[1:3]):
                source = self._expression_slot(branch, fact, f"{role}:branch:{index}")
                self._add_edge(source, target, self._step(fact, f"nhánh có thể của {expr.text}"))
            return target
        slot = self._expr(fact.id, role, expr.text)
        self._add_value(
            slot,
            AbstractValue(kind="unknown", value=expr.text),
            self._step(fact, f"chưa có mô hình cho biểu thức {expr.text}"),
        )
        return slot

    def _find_call(self, fact: SemanticFact, expression_text: str) -> CallFact | None:
        key = (fact.scope_id, fact.location.file, fact.location.line_start, expression_text)
        candidates = self.call_by_signature.get(key, [])
        if not candidates:
            candidates = self.call_by_location_text.get(
                (fact.location.file, fact.location.line_start, expression_text), []
            )
        return candidates[0] if candidates else None

    def _run_worklist(self) -> None:
        while self.queue:
            if self.metrics.worklist_iterations >= self.max_propagations:
                self.worklist_cutoff = True
                self.partial_reasons.append(
                    f"dataflow vượt giới hạn {self.max_propagations} lần truyền"
                )
                return
            slot, value_key = self.queue.popleft()
            self.metrics.worklist_iterations += 1
            value = self.values[slot][value_key]
            evidence = self.evidence[(slot, value_key)]
            for edge in self.edges.get(slot, []):
                self._add_value(edge.target, value, [*evidence, edge.evidence])
            for call in self.call_watchers.get(slot, []):
                self._handle_call_value(call, value, slot)
            for call_id in self.receiver_watchers.get(slot, set()):
                self._record_receiver_type(call_id, value)
            for attr, target, fact in self.attr_reads.get(slot, []):
                self._handle_attribute_read(value, attr, target, fact, slot)
            for attr, source, fact in self.attr_writes.get(slot, []):
                if value.kind == "instance":
                    self._add_edge(
                        source,
                        self._attr(value.value, attr),
                        self._step(fact, f"gán vào thuộc tính {value.value}.{attr}"),
                    )

    def _handle_attribute_read(
        self,
        value: AbstractValue,
        attribute: str,
        target_slot: str,
        fact: SemanticFact,
        receiver_slot: str,
    ) -> None:
        if value.kind == "instance":
            type_symbol = value.type_symbol
            method = self._find_method(type_symbol, attribute) if type_symbol else None
            if method:
                self._add_value(
                    target_slot,
                    AbstractValue(kind="symbol", value=method, symbol_kind="method",
                                  receiver_object_id=value.value, receiver_type=type_symbol),
                    [
                        *self.evidence.get((receiver_slot, value.key), []),
                        self._step(fact, f"{attribute} thuộc type {type_symbol}"),
                    ],
                )
            self._add_edge(
                self._attr(value.value, attribute),
                target_slot,
                self._step(fact, f"đọc thuộc tính {value.value}.{attribute}"),
            )
        elif value.kind == "symbol":
            full = f"{value.value}.{attribute}"
            if full in self.global_slots:
                for source in self.global_slots[full]:
                    self._add_edge(
                        source,
                        target_slot,
                        self._step(fact, f"đọc biến module {full}"),
                    )
            elif full in self.definitions or full in self.registry.callables or full in self.known_modules:
                kind = self._symbol_kind(full)
                self._add_value(
                    target_slot,
                    AbstractValue(kind="symbol", value=full, symbol_kind=kind),
                    self._step(fact, f"nối {attribute} thành {full}"),
                )
        elif value.kind in ("runtime", "unknown"):
            self._add_value(
                target_slot,
                AbstractValue(kind=value.kind, value=f"{value.value}.{attribute}"),
                self._step(fact, f"receiver của .{attribute} chưa xác định tĩnh"),
            )

    def _handle_call_value(self, call: CallFact, value: AbstractValue, callee_slot: str) -> None:
        if value.kind in ("runtime", "unknown"):
            if value.kind == "runtime":
                self.call_runtime[call.id].append(
                    self._step(call, f"callee {call.callee.text} phụ thuộc runtime")
                )
                self._add_value(
                    self._call_result(call.id),
                    AbstractValue(kind="runtime", value=call.expression_text),
                    self._step(call, "kết quả call chỉ biết lúc runtime"),
                )
            else:
                self._add_value(
                    self._call_result(call.id), AbstractValue(kind="unknown", value=call.expression_text),
                    self._step(call, "chưa xác định được kết quả call"),
                )
            return
        if value.kind != "symbol":
            return
        target = value.value
        if value.receiver_object_id:
            receiver_slot = self.receiver_slots.setdefault(call.id, f"bound-receiver:{call.id}")
            receiver = AbstractValue(kind="instance", value=value.receiver_object_id, type_symbol=value.receiver_type)
            self._add_value(receiver_slot, receiver, self._step(call, "method giữ object receiver khi truyền qua alias"))
            self._record_receiver_type(call.id, receiver)
        targets = self.call_targets[call.id]
        if target not in targets and len(targets) >= self.max_candidates:
            self.call_truncated.add(call.id)
            return
        targets.add(target)
        model = self.registry.callables.get(target)
        definition = self.definitions.get(target)
        if model and model.returns_symbol:
            self._add_value(
                self._call_result(call.id),
                AbstractValue(kind="symbol", value=model.returns_symbol, symbol_kind="class"),
                self._step(call, f"mô hình {target} trả class {model.returns_symbol}"),
            )
        if (model and model.kind == "class") or (
            definition is not None and definition.symbol_kind == "class"
        ):
            result_type = model.returns if model else target
            instance = AbstractValue(
                kind="instance",
                value=f"allocation:{call.id}",
                type_symbol=result_type or target,
            )
            self._add_value(
                self._call_result(call.id),
                instance,
                [
                    *self.evidence.get((callee_slot, value.key), []),
                    self._step(call, f"{target} tạo instance {result_type or target}"),
                ],
            )
            self._connect_constructor(call, result_type or target, instance)
            return
        if model and model.returns_runtime:
            self._add_value(
                self._call_result(call.id),
                AbstractValue(kind="runtime", value=f"return:{target}"),
                self._step(call, f"kết quả {target} phụ thuộc runtime"),
            )
        elif model and model.returns:
            self._add_value(
                self._call_result(call.id),
                AbstractValue(
                    kind="instance",
                    value=f"allocation:{call.id}",
                    type_symbol=model.returns,
                ),
                self._step(call, f"{target} trả về {model.returns}"),
            )
        if definition and definition.symbol_kind in ("function", "async_function"):
            self._connect_internal_call(call, target)
        elif target.rsplit(".", 1)[0] in self.definitions:
            self._connect_internal_call(call, target)

    def _connect_internal_call(self, call: CallFact, target: str) -> None:
        params = self.parameters.get(target, [])
        positional = [param for param in params if param.parameter_kind == "positional"]
        offset = 0
        if call.id in self.receiver_slots and positional and positional[0].name in ("self", "cls"):
            receiver = self.receiver_slots.get(call.id)
            if receiver is None:
                receiver = self._expression_slot(call.callee.base, call, "callee:base")
            self._add_edge(
                receiver,
                self.binding_slot_by_fact[positional[0].id],
                self._step(call, f"receiver truyền vào {target}.{positional[0].name}"),
            )
            offset = 1
        for source, parameter in zip(self.argument_slots.get(call.id, []), positional[offset:]):
            self._add_edge(
                source,
                self.binding_slot_by_fact[parameter.id],
                self._step(call, f"argument truyền vào parameter {target}.{parameter.name}"),
            )
        by_name = {param.name: param for param in params}
        for name, source in self.keyword_slots.get(call.id, {}).items():
            if name not in by_name:
                continue
            parameter = by_name[name]
            self._add_edge(
                source,
                self.binding_slot_by_fact[parameter.id],
                self._step(call, f"keyword argument truyền vào {target}.{name}"),
            )
        self._add_edge(
            self._return(target),
            self._call_result(call.id),
            self._step(call, f"return của {target} truyền về call site"),
        )

    def _connect_constructor(
        self, call: CallFact, type_symbol: str, instance: AbstractValue
    ) -> None:
        initializer = f"{type_symbol}.__init__"
        if initializer not in self.definitions:
            return
        params = [
            param
            for param in self.parameters.get(initializer, [])
            if param.parameter_kind == "positional"
        ]
        offset = 0
        if params and params[0].name in ("self", "cls"):
            self._add_value(
                self.binding_slot_by_fact[params[0].id],
                instance,
                self._step(call, f"object mới truyền vào {initializer}.{params[0].name}"),
            )
            offset = 1
        for source, parameter in zip(self.argument_slots.get(call.id, []), params[offset:]):
            self._add_edge(
                source,
                self.binding_slot_by_fact[parameter.id],
                self._step(call, f"constructor argument truyền vào {initializer}.{parameter.name}"),
            )
        by_name = {param.name: param for param in self.parameters.get(initializer, [])}
        for name, source in self.keyword_slots.get(call.id, {}).items():
            parameter = by_name.get(name)
            if parameter:
                self._add_edge(
                    source,
                    self.binding_slot_by_fact[parameter.id],
                    self._step(call, f"constructor keyword truyền vào {initializer}.{name}"),
                )

    def _finalize_calls(self) -> list[ResolvedCall]:
        result: list[ResolvedCall] = []
        for call in sorted(self.calls.values(), key=lambda item: item.id):
            targets = sorted(self.call_targets.get(call.id, set()))
            runtime_steps = self.call_runtime.get(call.id, [])
            incomplete_callee = any(
                value.kind in ("unknown", "runtime")
                for value in self.values.get(self.callee_slots.get(call.id), {}).values()
            )
            call_slots = [self.callee_slots.get(call.id), self.receiver_slots.get(call.id),
                          *self.argument_slots.get(call.id, []), *self.keyword_slots.get(call.id, {}).values()]
            truncated = call.id in self.call_truncated or self.worklist_cutoff or any(slot in self.truncated_slots for slot in call_slots)
            if len(targets) == 1 and not incomplete_callee and not truncated:
                status = "resolved"
                self.metrics.resolved_calls += 1
            elif targets:
                status = "candidates"
                self.metrics.candidate_calls += 1
            elif runtime_steps:
                status = "runtime"
                self.metrics.runtime_calls += 1
            else:
                status = "unresolved"
                self.metrics.unresolved_calls += 1
            if truncated:
                self.metrics.truncated_calls += 1
            if call.id in self.call_truncated:
                self.partial_reasons.append(
                    f"call {call.expression_text} vượt {self.max_candidates} candidates"
                )
            call_result = list(self.values.get(self._call_result(call.id), {}).values())
            evidence: list[EvidenceStep] = []
            callee_slot = self.callee_slots.get(call.id)
            for value in self.values.get(callee_slot, {}).values():
                evidence.extend(self.evidence.get((callee_slot, value.key), []))
            evidence.extend(runtime_steps)
            evidence = _dedupe_evidence(evidence)
            result.append(
                ResolvedCall(
                    call_fact_id=call.id,
                    caller_symbol=call.enclosing_function,
                    written_callee=call.callee.text,
                    status=status,
                    targets=targets,
                    receiver_types=sorted(self.call_receiver_types.get(call.id, set())),
                    callee_slot=callee_slot,
                    receiver_slot=self.receiver_slots.get(call.id),
                    argument_slots=list(self.argument_slots.get(call.id, [])),
                    keyword_slots=dict(self.keyword_slots.get(call.id, {})),
                    result_values=sorted(call_result, key=lambda item: item.key),
                    evidence=evidence[:MAX_EVIDENCE_STEPS],
                    reason=("phân tích bị cắt tại giới hạn; candidate chưa đầy đủ" if truncated else self._reason(status, call, targets)),
                    truncated=truncated,
                    location=call.location,
                )
            )
        return result

    def _record_receiver_type(self, call_id: str, value: AbstractValue) -> None:
        if value.kind == "instance" and value.type_symbol:
            self.call_receiver_types[call_id].add(value.type_symbol)

    def _reason(self, status: str, call: CallFact, targets: list[str]) -> str | None:
        if status == "resolved":
            return None
        if status == "candidates":
            return f"có {len(targets)} đích đã biết; còn nhiều khả năng hoặc thông tin chưa xác định"
        if status == "runtime":
            return "callee hoặc receiver phụ thuộc dữ liệu chỉ có lúc chạy"
        return f"không đủ binding/type để nối '{call.callee.text}'"

    def _find_method(self, type_symbol: str, method: str, seen: set[str] | None = None) -> str | None:
        for owner in self._linearization(type_symbol) or []:
            direct = f"{owner}.{method}"
            if direct in self.definitions:
                return direct
            model = self.registry.types.get(owner)
            if model and method in model.methods:
                return model.methods[method]
        return None

    def _linearization(self, symbol: str, seen: frozenset[str] = frozenset()) -> list[str] | None:
        """Thứ tự tìm method C3 của Python, bao gồm kế thừa hình thoi."""
        if symbol in seen or len(seen) > 64:
            return None
        if symbol in self.mro_cache:
            return self.mro_cache[symbol]
        library = self.registry.types.get(symbol)
        bases = self.internal_bases.get(symbol, list(library.bases) if library else [])
        sequences = []
        for base in bases:
            order = self._linearization(base, seen | {symbol})
            if order is None:
                self.mro_cache[symbol] = None
                return None
            sequences.append(list(order))
        sequences.append(list(bases))
        result = [symbol]
        while any(sequences):
            sequences = [sequence for sequence in sequences if sequence]
            candidate = next((sequence[0] for sequence in sequences
                              if not any(sequence[0] in other[1:] for other in sequences)), None)
            if candidate is None:
                self.mro_cache[symbol] = None
                return None
            result.append(candidate)
            for sequence in sequences:
                if sequence[0] == candidate:
                    sequence.pop(0)
        self.mro_cache[symbol] = result
        return result

    def _static_symbol(self, scope_id: str, expr: ExpressionIR) -> str | None:
        if expr.kind == "name":
            name = expr.name or expr.text
            scope = scope_id
            while scope:
                imports = self.import_by_scope_name.get((scope, name), [])
                if imports:
                    return imports[-1].imported_symbol
                definitions = self.definition_by_scope_name.get((scope, name), [])
                if definitions:
                    return definitions[-1].qualified_name
                scope = self.parent_scope.get(scope)
        if expr.kind == "attribute" and expr.base:
            base = self._static_symbol(scope_id, expr.base)
            return f"{base}.{expr.attribute}" if base else None
        return None

    def _resolve_type_annotation(self, scope_id: str, expr: ExpressionIR) -> str | None:
        if expr.kind == "literal" and isinstance(expr.literal, str):
            return self._static_symbol(scope_id, ExpressionIR(kind="name", name=expr.literal, text=expr.literal))
        if expr.kind == "subscript" and expr.elements:
            wrapper = self._static_symbol(scope_id, expr.base) if expr.base else None
            if wrapper in ("typing.Optional", "typing.Annotated"):
                first = expr.elements[0]
                if first.kind == "tuple" and first.elements:
                    first = first.elements[0]
                return self._resolve_type_annotation(scope_id, first)
            # list[Service] là container, không phải một instance Service.
            return None
        if expr.kind == "binary" and expr.elements:
            types = {self._resolve_type_annotation(scope_id, element) for element in expr.elements}
            types.discard(None)
            return next(iter(types)) if len(types) == 1 else None
        return self._static_symbol(scope_id, expr)

    def _lookup_vars(
        self, scope_id: str, name: str, use_fact: SemanticFact
    ) -> list[str]:
        scope: str | None = scope_id
        first_scope = True
        while scope:
            bindings = self.bindings.get((scope, name), [])
            if bindings:
                if first_scope:
                    eligible = [
                        item for item in bindings if self._is_before(item.fact, use_fact)
                    ]
                    if not eligible:
                        # Có assignment trong local scope nhưng chưa chạy tới nó:
                        # Python coi đây là local chưa khởi tạo, không rơi ra outer scope.
                        return []
                else:
                    # Không mô phỏng thời điểm gọi: outer scope có thể được đọc
                    # trước hoặc sau một lần rebind. Giữ mọi binding ứng viên.
                    return [item.slot for item in bindings]
                return self._reaching(eligible)

            parent = self.parent_scope.get(scope)
            if (
                first_scope
                and parent
                and self.scopes.get(scope)
                and self.scopes[scope].scope_kind == "function"
                and self.scopes.get(parent)
                and self.scopes[parent].scope_kind == "class"
            ):
                # Bare name trong method không tra namespace của class.
                parent = self.parent_scope.get(parent)
            scope = parent
            first_scope = False
        return []

    @staticmethod
    def _reaching(bindings: list[_Binding]) -> list[str]:
        if not bindings:
            return []
        last_unconditional = -1
        for index, binding in enumerate(bindings):
            if not binding.conditional:
                last_unconditional = index
        if not bindings[-1].conditional:
            return [bindings[-1].slot]
        start = max(last_unconditional, 0)
        return [binding.slot for binding in bindings[start:]]

    @staticmethod
    def _is_before(binding: SemanticFact, use: SemanticFact) -> bool:
        if binding.location.file != use.location.file:
            return True
        if binding.location.line_end < use.location.line_start:
            return True
        return (
            binding.location.line_end == use.location.line_start
            and binding.location.column_end <= use.location.column_start
        )

    @staticmethod
    def _location_key(fact: SemanticFact) -> tuple[int, int, int, int, str]:
        return (
            fact.location.line_start,
            fact.location.column_start,
            fact.location.line_end,
            fact.location.column_end,
            fact.id,
        )

    def _add_edge(self, source: str, target: str, evidence: EvidenceStep) -> None:
        key = (source, target)
        if key in self.edge_keys:
            return
        self.edge_keys.add(key)
        self.edges[source].append(_Edge(target, evidence))
        self.metrics.constraints += 1
        for value in list(self.values.get(source, {}).values()):
            current = self.evidence.get((source, value.key), [])
            self._add_value(target, value, [*current, evidence])

    def _add_value(
        self,
        slot: str,
        value: AbstractValue,
        evidence: EvidenceStep | list[EvidenceStep],
    ) -> None:
        if value.key in self.values[slot]:
            return
        if len(self.values[slot]) >= MAX_VALUES_PER_SLOT:
            if slot not in self.truncated_slots:
                self.partial_reasons.append(f"slot {slot} vượt giới hạn {MAX_VALUES_PER_SLOT} giá trị")
                self.truncated_slots.add(slot)
            return
        self.values[slot][value.key] = value
        steps = evidence if isinstance(evidence, list) else [evidence]
        self.evidence[(slot, value.key)] = _dedupe_evidence(steps)[-MAX_EVIDENCE_STEPS:]
        self.queue.append((slot, value.key))
        self.metrics.propagated_values += 1

    def _step(self, fact: SemanticFact, description: str) -> EvidenceStep:
        return EvidenceStep(description=description, location=fact.location, fact_id=fact.id)

    def _propagate_truncation(self) -> None:
        """Chỉ hạ độ chắc chắn ở phần phụ thuộc vào slot đã bị cắt."""
        dependents: dict[str, set[str]] = defaultdict(set)
        for source, edges in self.edges.items():
            dependents[source].update(edge.target for edge in edges)
        for source, reads in self.attr_reads.items():
            dependents[source].update(target for _, target, _ in reads)
        for call in self.calls.values():
            result = self._call_result(call.id)
            for slot in [self.callee_slots.get(call.id), self.receiver_slots.get(call.id),
                         *self.argument_slots.get(call.id, []), *self.keyword_slots.get(call.id, {}).values()]:
                if slot:
                    dependents[slot].add(result)
            if call.id in self.call_truncated:
                self.truncated_slots.add(result)
        queue = deque(sorted(self.truncated_slots))
        while queue:
            for target in dependents.get(queue.popleft(), ()):
                if target not in self.truncated_slots:
                    self.truncated_slots.add(target)
                    queue.append(target)

    def _symbol_kind(self, symbol: str) -> str:
        definition = self.definitions.get(symbol)
        if definition:
            return "class" if definition.symbol_kind == "class" else "function"
        model = self.registry.callables.get(symbol)
        if model:
            return "class" if model.kind == "class" else "external"
        return "external"

    @staticmethod
    def _var(scope_id: str, name: str) -> str:
        return f"var:{scope_id}:{name}"

    @staticmethod
    def _return(function: str) -> str:
        return f"return:{function}"

    @staticmethod
    def _call_result(call_id: str) -> str:
        return f"call-result:{call_id}"

    @staticmethod
    def _attr(type_symbol: str, name: str) -> str:
        return f"attribute:{type_symbol}:{name}"

    @staticmethod
    def _expr(fact_id: str, role: str, text: str) -> str:
        digest = hashlib.sha256(text.encode("utf-8", errors="surrogatepass")).hexdigest()[:16]
        return f"expr:{fact_id}:{role}:{digest}"


def _dedupe_evidence(steps: list[EvidenceStep]) -> list[EvidenceStep]:
    found: list[EvidenceStep] = []
    seen: set[tuple[str, str | None]] = set()
    for step in steps:
        key = (step.description, step.fact_id)
        if key not in seen:
            seen.add(key)
            found.append(step)
    return found


def resolve_program(
    program: SemanticProgram,
    registry: SemanticRegistry | None = None,
    max_candidates: int = MAX_CANDIDATES_PER_CALL,
    max_propagations: int = MAX_PROPAGATIONS,
) -> ResolutionResult:
    return DataflowResolver(program, registry, max_candidates, max_propagations).run()
