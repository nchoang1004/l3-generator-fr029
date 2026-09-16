"""Python AST → Common Semantic IR, không chứa kiến thức framework."""

from __future__ import annotations

import ast
import hashlib
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator

from l3gen.languages.python.parser import ParsedFile
from l3gen.models.semantic import (
    AssignmentFact,
    CallFact,
    DecoratorFact,
    DefinitionFact,
    ExpressionIR,
    ImportFact,
    InheritanceFact,
    ParameterFact,
    ReturnFact,
    ScopeFact,
    SemanticLocation,
    SemanticModule,
    SemanticProgram,
)

FRONTEND_VERSION = "python-ast-v2"


@dataclass(frozen=True)
class _Scope:
    id: str
    kind: str
    qualified_name: str


def build_semantic_program(
    files: list[ParsedFile], module_of: dict[str, str]
) -> SemanticProgram:
    modules = [_ModuleExtractor(parsed, module_of[parsed.rel_path]).extract() for parsed in files]
    return SemanticProgram(frontend_version=FRONTEND_VERSION, modules=modules)


class _ModuleExtractor(ast.NodeVisitor):
    def __init__(self, parsed: ParsedFile, module: str) -> None:
        self.parsed = parsed
        self.module = module
        root_name = module or parsed.rel_path
        self.scopes = [_Scope(f"module:{root_name}", "module", root_name)]
        self.conditions: list[str] = []
        self.try_depth = 0
        self.context = "body"
        self.facts = []
        self.analysis_notes: list[str] = []

    @property
    def scope(self) -> _Scope:
        return self.scopes[-1]

    @property
    def enclosing_function(self) -> str | None:
        found = next((scope for scope in reversed(self.scopes) if scope.kind == "function"), None)
        return found.qualified_name if found else None

    @property
    def enclosing_class(self) -> str | None:
        found = next((scope for scope in reversed(self.scopes) if scope.kind == "class"), None)
        return found.qualified_name if found else None

    def extract(self) -> SemanticModule:
        location = SemanticLocation(
            file=self.parsed.rel_path,
            line_start=0,
            column_start=0,
            line_end=max(self.parsed.line_count, 0),
            column_end=0,
        )
        self.facts.append(
            ScopeFact(
                id=self._id(location, "scope", self.scope.id),
                scope_id=self.scope.id,
                location=location,
                frontend_version=FRONTEND_VERSION,
                scope_kind="module",
                name=self.module or self.parsed.rel_path,
                qualified_name=self.module or self.parsed.rel_path,
                parent_scope_id=None,
            )
        )
        self.visit(self.parsed.tree)
        self.facts.sort(key=lambda fact: (fact.location.line_start, fact.location.column_start, fact.id))
        return SemanticModule(module=self.module, file=self.parsed.rel_path, facts=self.facts,
                              analysis_notes=sorted(set(self.analysis_notes)))

    def generic_visit(self, node: ast.AST) -> None:
        if isinstance(node, (ast.Global, ast.Nonlocal, ast.Match, ast.With, ast.AsyncWith,
                             ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)):
            self.analysis_notes.append(
                f"{self.parsed.rel_path}:{getattr(node, 'lineno', 0)}: "
                f"{type(node).__name__} chưa có đầy đủ mô hình binding/control flow"
            )
        super().generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.analysis_notes.append(f"{self.parsed.rel_path}:{node.lineno}: vòng lặp chưa được mô phỏng từng lượt")
        self.conditions.append(f"trong vòng lặp {_text(node.target)} in {_text(node.iter)} (chưa biết số lượt)")
        self.generic_visit(node)
        self.conditions.pop()

    visit_AsyncFor = visit_For

    def visit_While(self, node: ast.While) -> None:
        self.analysis_notes.append(f"{self.parsed.rel_path}:{node.lineno}: vòng while chưa được mô phỏng từng lượt")
        self.conditions.append(f"while {_text(node.test)} (chưa biết số lượt)")
        self.generic_visit(node)
        self.conditions.pop()

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            local = alias.asname or alias.name.split(".")[0]
            imported = alias.name if alias.asname else alias.name.split(".")[0]
            self.facts.append(
                ImportFact(
                    **self._base(node, "import", local),
                    local_name=local,
                    imported_symbol=imported,
                )
            )

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = self.module
        if self.parsed.rel_path.endswith(("/__init__.py", "/__init__.pyi")):
            module += ".__init__"
        base = _resolve_relative(module, node.level, node.module)
        for alias in node.names:
            local = alias.asname or alias.name
            imported = f"{base}.{alias.name}" if base else alias.name
            wildcard = alias.name == "*"
            self.facts.append(
                ImportFact(
                    **self._base(node, "import", local),
                    local_name=local,
                    imported_symbol=imported,
                    is_wildcard=wildcard,
                    completeness="partial" if wildcard else "full",
                    reason="wildcard import cần bước binding riêng" if wildcard else None,
                )
            )

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        qname = self._qualified(node.name)
        self.facts.append(
            DefinitionFact(
                **self._base(node, "definition", node.name),
                name=node.name,
                qualified_name=qname,
                symbol_kind="class",
                conditions=list(self.conditions),
            )
        )
        self.facts.append(
            InheritanceFact(
                **self._base(node, "inheritance", qname),
                class_symbol=qname,
                bases=[_expression(base) for base in node.bases],
                keywords={kw.arg or "**": _expression(kw.value) for kw in node.keywords},
            )
        )
        self._visit_decorators(node.decorator_list, qname)
        with self._temporary_context("class_base"):
            for expression in [*node.bases, *(kw.value for kw in node.keywords)]:
                self.visit(expression)
        with self._nested_scope("class", qname, node):
            for statement in node.body:
                self.visit(statement)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_function(node, "function")

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_function(node, "async_function")

    def _visit_function(self, node, symbol_kind: str) -> None:
        qname = self._qualified(node.name)
        self.facts.append(
            DefinitionFact(
                **self._base(node, "definition", node.name),
                name=node.name,
                qualified_name=qname,
                symbol_kind=symbol_kind,
                conditions=list(self.conditions),
                return_annotation=_expression(node.returns) if node.returns is not None else None,
            )
        )
        self._visit_decorators(node.decorator_list, qname)
        with self._temporary_context("default"):
            for default in [*node.args.defaults, *(d for d in node.args.kw_defaults if d)]:
                self.visit(default)
        with self._nested_scope("function", qname, node):
            self._add_parameters(node, qname)
            for statement in node.body:
                self.visit(statement)

    def _visit_decorators(self, decorators: list[ast.expr], owner: str) -> None:
        with self._temporary_context("decorator"):
            for decorator in decorators:
                self.facts.append(
                    DecoratorFact(
                        **self._base(decorator, "decorator", owner),
                        owner_symbol=owner,
                        expression=_expression(decorator),
                    )
                )
                self.visit(decorator)

    def _add_parameters(self, node, function_symbol: str) -> None:
        positional = [*node.args.posonlyargs, *node.args.args]
        defaults = [None] * (len(positional) - len(node.args.defaults)) + list(node.args.defaults)
        for position, (arg, default) in enumerate(zip(positional, defaults)):
            self._add_parameter(arg, function_symbol, position, "positional", default)
        offset = len(positional)
        for position, (arg, default) in enumerate(
            zip(node.args.kwonlyargs, node.args.kw_defaults), start=offset
        ):
            self._add_parameter(arg, function_symbol, position, "keyword_only", default)
        if node.args.vararg:
            self._add_parameter(node.args.vararg, function_symbol, -1, "vararg", None)
        if node.args.kwarg:
            self._add_parameter(node.args.kwarg, function_symbol, -1, "kwarg", None)

    def _add_parameter(self, arg, function_symbol, position, kind, default) -> None:
        self.facts.append(
            ParameterFact(
                **self._base(arg, "parameter", f"{function_symbol}:{arg.arg}"),
                function_symbol=function_symbol,
                name=arg.arg,
                position=position,
                parameter_kind=kind,
                annotation=_expression(arg.annotation) if arg.annotation else None,
                default=_expression(default) if default else None,
            )
        )

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            for actual_target, actual_value in _assignment_pairs(target, node.value):
                self.facts.append(
                    AssignmentFact(
                        **self._base(node, "assignment", _text(actual_target)),
                        target=_expression(actual_target),
                        value=_expression(actual_value),
                        conditions=list(self.conditions),
                        enclosing_function=self.enclosing_function,
                        enclosing_class=self.enclosing_class,
                    )
                )
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self.facts.append(
            AssignmentFact(
                **self._base(node, "assignment", _text(node.target)),
                target=_expression(node.target),
                value=_expression(node.value),
                annotation=_expression(node.annotation),
                has_value=node.value is not None,
                conditions=list(self.conditions),
                enclosing_function=self.enclosing_function,
                enclosing_class=self.enclosing_class,
            )
        )
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        value = ast.BinOp(left=node.target, op=node.op, right=node.value)
        value.lineno = node.lineno
        value.col_offset = node.col_offset
        value.end_lineno = getattr(node, "end_lineno", node.lineno)
        value.end_col_offset = getattr(node, "end_col_offset", node.col_offset)
        self.facts.append(
            AssignmentFact(
                **self._base(node, "assignment", _text(node.target)),
                target=_expression(node.target),
                value=_expression(value),
                conditions=list(self.conditions),
                enclosing_function=self.enclosing_function,
                enclosing_class=self.enclosing_class,
            )
        )
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        self.facts.append(
            CallFact(
                **self._base(node, "call", _text(node.func)),
                expression_text=_text(node),
                callee=_expression(node.func),
                arguments=[_expression(arg) for arg in node.args],
                keywords={kw.arg or "**": _expression(kw.value) for kw in node.keywords},
                conditions=list(self.conditions),
                enclosing_function=self.enclosing_function,
                enclosing_class=self.enclosing_class,
                inside_try_except=self.try_depth > 0,
                context=self.context,
            )
        )
        self.generic_visit(node)

    def visit_Return(self, node: ast.Return) -> None:
        if self.enclosing_function:
            self.facts.append(
                ReturnFact(
                    **self._base(node, "return", self.enclosing_function),
                    function_symbol=self.enclosing_function,
                    value=_expression(node.value) if node.value else None,
                    conditions=list(self.conditions),
                )
            )
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        condition = _text(node.test)
        self.visit(node.test)
        self.conditions.append(condition)
        for statement in node.body:
            self.visit(statement)
        self.conditions.pop()
        if node.orelse:
            self.conditions.append(f"not ({condition})")
            for statement in node.orelse:
                self.visit(statement)
            self.conditions.pop()

    def visit_Try(self, node: ast.Try) -> None:
        self.try_depth += 1
        for statement in node.body:
            self.visit(statement)
        self.try_depth -= 1
        for handler in node.handlers:
            self.visit(handler)
        for statement in [*node.orelse, *node.finalbody]:
            self.visit(statement)

    @contextmanager
    def _nested_scope(self, kind: str, qname: str, node: ast.AST) -> Iterator[None]:
        scope = _Scope(f"{kind}:{qname}", kind, qname)
        parent = self.scope
        self.scopes.append(scope)
        self.facts.append(
            ScopeFact(
                **self._base(node, "scope", scope.id),
                scope_kind=kind,
                name=qname.rsplit(".", 1)[-1],
                qualified_name=qname,
                parent_scope_id=parent.id,
            )
        )
        try:
            yield
        finally:
            self.scopes.pop()

    @contextmanager
    def _temporary_context(self, context: str) -> Iterator[None]:
        previous = self.context
        self.context = context
        try:
            yield
        finally:
            self.context = previous

    def _qualified(self, name: str) -> str:
        if self.scope.kind == "module":
            prefix = self.module
        else:
            prefix = self.scope.qualified_name
        return f"{prefix}.{name}" if prefix else name

    def _id(self, location: SemanticLocation, kind: str, discriminator: str) -> str:
        raw = (
            f"python|{self.parsed.rel_path}|{location.line_start}|{location.column_start}|"
            f"{kind}|{discriminator}|{self.scope.id}"
        )
        return f"py:{hashlib.sha256(raw.encode()).hexdigest()[:20]}"

    def _base(self, node: ast.AST, kind: str, discriminator: str) -> dict:
        location = _location(self.parsed.rel_path, node)
        return {
            "id": self._id(location, kind, discriminator),
            "scope_id": self.scope.id,
            "location": location,
            "frontend_version": FRONTEND_VERSION,
        }


def _resolve_relative(module: str, level: int, imported: str | None) -> str:
    if level == 0:
        return imported or ""
    package = module.split(".")[:-1] if module else []
    for _ in range(level - 1):
        package = package[:-1]
    base = ".".join(package)
    return f"{base}.{imported}" if base and imported else (imported or base)


def _location(rel_path: str, node: ast.AST) -> SemanticLocation:
    return SemanticLocation(
        file=rel_path,
        line_start=getattr(node, "lineno", 0),
        column_start=getattr(node, "col_offset", 0),
        line_end=getattr(node, "end_lineno", getattr(node, "lineno", 0)),
        column_end=getattr(node, "end_col_offset", getattr(node, "col_offset", 0)),
    )


def _text(node: ast.AST) -> str:
    try:
        return ast.unparse(node)
    except Exception:  # pragma: no cover - chỉ cho AST mở rộng không chuẩn
        return node.__class__.__name__


def _assignment_pairs(target: ast.expr, value: ast.expr):
    """Tách destructuring tĩnh như ``a, b = x, y`` thành hai phép gán."""
    if (
        isinstance(target, (ast.Tuple, ast.List))
        and isinstance(value, (ast.Tuple, ast.List))
        and len(target.elts) == len(value.elts)
    ):
        pairs = []
        for child_target, child_value in zip(target.elts, value.elts):
            pairs.extend(_assignment_pairs(child_target, child_value))
        return pairs
    return [(target, value)]


def _expression(node: ast.expr | None) -> ExpressionIR:
    if node is None:
        return ExpressionIR(kind="unknown", text="None")
    if isinstance(node, ast.Name):
        return ExpressionIR(kind="name", text=node.id, name=node.id)
    if isinstance(node, ast.Attribute):
        return ExpressionIR(
            kind="attribute",
            text=_text(node),
            base=_expression(node.value),
            attribute=node.attr,
        )
    if isinstance(node, ast.Call):
        return ExpressionIR(
            kind="call",
            text=_text(node),
            source_line=node.lineno,
            source_column=node.col_offset,
            callee=_expression(node.func),
            arguments=[_expression(arg) for arg in node.args],
            keywords={kw.arg or "**": _expression(kw.value) for kw in node.keywords},
        )
    if isinstance(node, ast.Constant):
        value = node.value if isinstance(node.value, (str, int, float, bool)) else None
        return ExpressionIR(kind="literal", text=repr(node.value), literal=value)
    if isinstance(node, ast.JoinedStr):
        return ExpressionIR(kind="formatted_string", text=_text(node), elements=[
            _expression(value) if isinstance(value, ast.Constant)
            else ExpressionIR(kind="unknown", text=_text(value.value))
            for value in node.values
        ])
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        kind = "list" if isinstance(node, (ast.List, ast.Set)) else "tuple"
        return ExpressionIR(kind=kind, text=_text(node), elements=[_expression(e) for e in node.elts])
    if isinstance(node, ast.Dict):
        elements = []
        for key, value in zip(node.keys, node.values):
            if key is not None:
                elements.extend([_expression(key), _expression(value)])
        return ExpressionIR(kind="dict", text=_text(node), elements=elements)
    if isinstance(node, ast.Subscript):
        return ExpressionIR(
            kind="subscript", text=_text(node), base=_expression(node.value), elements=[_expression(node.slice)]
        )
    if isinstance(node, ast.BinOp):
        return ExpressionIR(
            kind="binary", text=_text(node), operator=type(node.op).__name__,
            elements=[_expression(node.left), _expression(node.right)]
        )
    if isinstance(node, ast.IfExp):
        return ExpressionIR(
            kind="conditional",
            text=_text(node),
            elements=[_expression(node.test), _expression(node.body), _expression(node.orelse)],
        )
    return ExpressionIR(kind="unknown", text=_text(node))
