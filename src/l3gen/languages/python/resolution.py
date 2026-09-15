"""Luật riêng của Python: tên module, đọc import, đoán kiểu biến.

Phần khung chung nằm ở core/resolution. File này chỉ chứa những thứ đúng với
Python và sai với ngôn ngữ khác.
"""

import ast
import builtins
from dataclasses import dataclass, field
from pathlib import PurePosixPath

from l3gen.core.resolution.inheritance import ClassRecord, ClimbResult, find_method_owner
from l3gen.core.resolution.symbol_table import (
    KIND_ASSIGN,
    KIND_CLASS,
    KIND_FUNCTION,
    KIND_METHOD,
    Definition,
    DefinitionIndex,
    FileScope,
    ImportTables,
)
from l3gen.languages.python.parser import ParsedFile
from l3gen.models.iam import Reference

FUNCTION_NODES = (ast.FunctionDef, ast.AsyncFunctionDef)

MAX_ALIAS_HOPS = 5
"""Số nhịp tối đa khi đi theo bí danh kiểu, chặn bí danh vòng."""


SOURCE_ROOT_DIRS = ("src",)


def module_name_for(rel_path: str, package_dirs: set[str]) -> str:
    """Đổi đường dẫn file thành tên module Python.

        app/services/order.py  ->  app.services.order
        app/__init__.py        ->  app
        src/app/main.py        ->  app.main   (src/ không phải package)

    Quy ước src/: thư mục tên "src" ở ngoài cùng mà không có __init__.py thì được
    coi là gốc source, không tính vào tên module. Đây là layout rất phổ biến.
    """
    path = PurePosixPath(rel_path)
    parts = list(path.parts[:-1])

    if parts and parts[0] in SOURCE_ROOT_DIRS and parts[0] not in package_dirs:
        parts = parts[1:]

    if path.stem == "__init__":
        return ".".join(parts)
    return ".".join([*parts, path.stem])


def find_package_dirs(rel_paths: list[str]) -> set[str]:
    """Thư mục nào có __init__.py thì là package."""
    return {
        PurePosixPath(p).parent.as_posix()
        for p in rel_paths
        if PurePosixPath(p).name == "__init__.py"
    }


def build_definition_index(files: list[ParsedFile]) -> tuple[DefinitionIndex, dict[str, str]]:
    """Dựng bảng 1 — danh bạ. Trả về kèm map file -> tên module."""
    package_dirs = find_package_dirs([f.rel_path for f in files])
    index = DefinitionIndex()
    module_of: dict[str, str] = {}

    for parsed in files:
        module = module_name_for(parsed.rel_path, package_dirs)
        module_of[parsed.rel_path] = module
        if module:
            index.known_modules.add(module)
            parts = module.split(".")
            for i in range(1, len(parts)):
                index.known_modules.add(".".join(parts[:i]))

        for node in parsed.tree.body:
            _index_top_level(node, module, parsed.rel_path, index)

    return index, module_of


def _index_top_level(node: ast.stmt, module: str, rel_path: str, index: DefinitionIndex) -> None:
    prefix = f"{module}." if module else ""

    if isinstance(node, ast.ClassDef):
        index.add(Definition(f"{prefix}{node.name}", rel_path, node.lineno, KIND_CLASS))
        for child in node.body:
            if isinstance(child, FUNCTION_NODES):
                index.add(
                    Definition(
                        f"{prefix}{node.name}.{child.name}", rel_path, child.lineno, KIND_METHOD
                    )
                )

    elif isinstance(node, FUNCTION_NODES):
        index.add(Definition(f"{prefix}{node.name}", rel_path, node.lineno, KIND_FUNCTION))

    elif isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                index.add(
                    Definition(f"{prefix}{target.id}", rel_path, node.lineno, KIND_ASSIGN)
                )


def build_import_tables(files: list[ParsedFile], module_of: dict[str, str]) -> ImportTables:
    """Dựng bảng 2 — tên gọi riêng cho từng file."""
    tables = ImportTables()

    for parsed in files:
        module = module_of[parsed.rel_path]
        scope = FileScope(rel_path=parsed.rel_path, module_name=module)
        prefix = f"{module}." if module else ""

        # Tên do chính file này định nghĩa.
        for node in parsed.tree.body:
            if isinstance(node, (ast.ClassDef, *FUNCTION_NODES)):
                scope.names[node.name] = f"{prefix}{node.name}"
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        scope.names[target.id] = f"{prefix}{target.id}"

        # Tên lấy về qua import. Ghi đè tên cùng loại ở trên là đúng thứ tự Python
        # chỉ khi import đứng sau; ở đây import luôn đứng đầu file nên không đè.
        for node in ast.walk(parsed.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    local = alias.asname or alias.name.split(".")[0]
                    target = alias.name if alias.asname else alias.name.split(".")[0]
                    scope.names[local] = target
            elif isinstance(node, ast.ImportFrom):
                base = _resolve_relative(module, node.level, node.module)
                for alias in node.names:
                    if alias.name == "*":
                        scope.has_wildcard_import = True
                        continue
                    local = alias.asname or alias.name
                    scope.names[local] = f"{base}.{alias.name}" if base else alias.name

        tables.by_file[parsed.rel_path] = scope

    return tables


def _resolve_relative(module: str, level: int, imported: str | None) -> str:
    """Đổi import tương đối (`from .order import X`) thành tên đầy đủ."""
    if level == 0:
        return imported or ""

    parts = module.split(".") if module else []
    # level=1 nghĩa là package chứa file này.
    package = parts[:-1] if parts else []
    for _ in range(level - 1):
        package = package[:-1]

    base = ".".join(package)
    if imported:
        return f"{base}.{imported}" if base else imported
    return base


# ---------------------------------------------------------------------------
# Nối lời gọi: từ `svc.confirm()` ra "hàm nào, file nào"
# ---------------------------------------------------------------------------

BUILTIN_NAMES = frozenset(dir(builtins))

EXTERNAL_REASON = "thuộc thư viện ngoài, ngoài phạm vi repo"
"""Đánh dấu lời gọi ra thư viện thứ ba. Đây là phân loại ĐÚNG, không phải
thất bại — dùng để tách nhóm khi báo cáo tỷ lệ nối được."""


def is_external(reference: Reference) -> bool:
    return bool(reference.reason) and EXTERNAL_REASON in reference.reason


def build_class_records(
    files: list[ParsedFile], module_of: dict[str, str]
) -> dict[str, ClassRecord]:
    """Dựng bảng class: tên cha là gì, có sẵn những method nào."""
    classes: dict[str, ClassRecord] = {}

    for parsed in files:
        module = module_of[parsed.rel_path]
        prefix = f"{module}." if module else ""
        for node in parsed.tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            qname = f"{prefix}{node.name}"
            classes[qname] = ClassRecord(
                qualified_name=qname,
                rel_path=parsed.rel_path,
                line=node.lineno,
                base_names=[t for t in (dotted_name(b) for b in node.bases) if t],
                method_names={
                    c.name for c in node.body if isinstance(c, FUNCTION_NODES)
                },
            )
    return classes


def dotted_name(node: ast.expr) -> str | None:
    """Đổi `a.b.c` trong cây cú pháp thành chuỗi "a.b.c". None nếu không phải tên."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dotted_name(node.value)
        return f"{base}.{node.attr}" if base else None
    return None


@dataclass
class Resolver:
    """Gộp hai bảng tra cứu lại thành một chỗ để hỏi."""

    index: DefinitionIndex
    tables: ImportTables
    classes: dict[str, ClassRecord]
    function_returns: dict[str, ast.expr | None] = field(default_factory=dict)
    assign_values: dict[str, tuple[str, ast.expr]] = field(default_factory=dict)
    external_origin: set[str] = field(default_factory=set)
    """Tên gán từ kết quả gọi thư viện ngoài, ví dụ `log = logging.getLogger(...)`.
    Không biết chính xác nó là class gì, nhưng biết chắc mọi lời gọi trên nó đều
    ra khỏi repo. Nói "gọi thư viện ngoài" đúng hơn "không biết đây là gì"."""

    def return_annotation_of(self, qualified_name: str) -> ast.expr | None:
        return self.function_returns.get(qualified_name)

    def resolve_type(self, scope: FileScope, written_name: str, depth: int = 0) -> str | None:
        """Như qualify(), nhưng đi tiếp qua bí danh kiểu.

        FastAPI hiện đại hay viết `SessionDep = Annotated[Session, Depends(get_db)]`
        rồi dùng `session: SessionDep`. Không đi tiếp một nhịp thì mọi lời gọi trên
        `session` đều thành "không biết là gì".
        """
        qname = self.qualify(scope, written_name)
        if qname is None or depth >= MAX_ALIAS_HOPS:
            return qname

        entry = self.assign_values.get(qname)
        if entry is None:
            return qname

        rel_path, value = entry
        inner = _alias_target(value)
        alias_scope = self.tables.for_file(rel_path)
        if inner is None or alias_scope is None:
            return qname
        return self.resolve_type(alias_scope, inner, depth + 1) or qname

    def qualify(self, scope: FileScope, written_name: str) -> str | None:
        """Tên viết trong file này ứng với tên đầy đủ nào.

        Xử lý cả tên nhiều đoạn: `models.Order` -> tra `models` rồi ghép `.Order`.
        """
        direct = scope.resolve(written_name)
        if direct:
            return direct
        head, _, rest = written_name.partition(".")
        head_target = scope.resolve(head)
        if head_target and rest:
            return f"{head_target}.{rest}"
        return None

    def resolve_base_of(self, record: ClassRecord, base_name: str) -> str | None:
        """Tên class cha -> tên đầy đủ, dùng bảng tên gọi CỦA FILE chứa class con."""
        scope = self.tables.for_file(record.rel_path)
        return self.qualify(scope, base_name) if scope else None

    def find_method(self, class_qname: str, method: str) -> ClimbResult:
        record = self.classes.get(class_qname)
        if record is None:
            return ClimbResult(reason=f"không tìm thấy class '{class_qname}' trong repo")
        return find_method_owner(record, method, self.classes, self.resolve_base_of)


# ---------------------------------------------------------------------------
# Bước 1 của mục 15.2: đoán kiểu biến
# ---------------------------------------------------------------------------

def annotation_name(node: ast.expr | None) -> str | None:
    """Lấy tên class từ chú thích kiểu. Bỏ lớp bọc Optional/list/Annotated."""
    if node is None:
        return None
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value.split("[")[0].strip() or None
    if isinstance(node, ast.Subscript):
        return annotation_name(node.slice) if _is_annotated(node) else None
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        # "OrderService | None" -> lấy vế không phải None
        for side in (node.left, node.right):
            if not (isinstance(side, ast.Constant) and side.value is None):
                return annotation_name(side)
        return None
    if isinstance(node, ast.Tuple) and node.elts:
        return annotation_name(node.elts[0])
    return dotted_name(node)


def _alias_target(value: ast.expr) -> str | None:
    """Phép gán này có phải bí danh kiểu không, và trỏ tới tên nào.

        SessionDep = Annotated[Session, Depends(get_db)]  ->  "Session"
        UserAlias  = User                                 ->  "User"
        Base       = declarative_base()                   ->  None (không phải bí danh)
    """
    if isinstance(value, ast.Name):
        return value.id
    if isinstance(value, ast.Subscript) and _is_annotated(value):
        return annotation_name(value.slice)
    return None


def _is_annotated(node: ast.Subscript) -> bool:
    head = dotted_name(node.value)
    return bool(head) and head.split(".")[-1] == "Annotated"


def _instantiated_class(value: ast.expr | None) -> str | None:
    """`OrderService()` -> "OrderService". None nếu không phải lời gọi khởi tạo."""
    if isinstance(value, ast.Call):
        return dotted_name(value.func)
    return None


def infer_variable_types(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    scope: FileScope,
    resolver: "Resolver",
) -> dict[str, str]:
    """Đoán kiểu các biến trong một hàm. Chỉ nhận bốn dạng, ngoài ra bỏ qua.

    Ghi nhận cả class thuộc thư viện ngoài. Biết `session` là `sqlmodel.Session`
    là thông tin có ích, dù không đọc được bên trong nó: nói "gọi ra thư viện
    ngoài" đúng hơn hẳn "không biết session là gì".

    Bỏ qua là kết quả ĐÚNG: thà nói không biết còn hơn trỏ nhầm file.
    """
    types: dict[str, str] = {}

    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]

    # Dạng 1 — chú thích kiểu trên tham số.
    for arg in all_args:
        written = annotation_name(arg.annotation)
        qname = resolver.resolve_type(scope, written) if written else None
        if qname:
            types[arg.arg] = qname

    # Dạng 3 — Depends(get_service): tra hàm đó xem khai báo trả về gì.
    positional = [*args.posonlyargs, *args.args]
    paired = list(zip(positional[len(positional) - len(args.defaults):], args.defaults))
    paired += list(zip(args.kwonlyargs, args.kw_defaults))
    for arg, default in paired:
        if arg.arg in types or default is None:
            continue
        qname = _depends_return_type(default, scope, resolver)
        if qname:
            types[arg.arg] = qname

    # Dạng 2 — gán trực tiếp `svc = OrderService()`.
    for node in ast.walk(func):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            written = annotation_name(node.annotation)
            qname = resolver.resolve_type(scope, written) if written else None
            if qname:
                types.setdefault(node.target.id, qname)
        elif isinstance(node, ast.Assign):
            written = _instantiated_class(node.value)
            qname = resolver.qualify(scope, written) if written else None
            if not qname:
                continue
            for target in node.targets:
                if isinstance(target, ast.Name):
                    types.setdefault(target.id, qname)

    return types


def _depends_return_type(
    default: ast.expr, scope: FileScope, resolver: "Resolver"
) -> str | None:
    """`Depends(get_service)` -> kiểu trả về khai báo của get_service."""
    if not isinstance(default, ast.Call):
        return None
    callee = dotted_name(default.func)
    if not callee or callee.split(".")[-1] != "Depends" or not default.args:
        return None

    provider = dotted_name(default.args[0])
    provider_qname = resolver.qualify(scope, provider) if provider else None
    if not provider_qname:
        return None

    definition = resolver.index.get(provider_qname)
    if definition is None:
        return None

    returns = resolver.return_annotation_of(provider_qname)
    written = annotation_name(returns)
    return resolver.resolve_type(scope, written) if written else None


def infer_self_attributes(
    class_node: ast.ClassDef, scope: FileScope, resolver: "Resolver"
) -> dict[str, str]:
    """Dạng 4 — `self.repo = OrderRepository()` trong __init__."""
    attrs: dict[str, str] = {}
    for member in class_node.body:
        if not (isinstance(member, FUNCTION_NODES) and member.name == "__init__"):
            continue
        for node in ast.walk(member):
            target, value = None, None
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target, value = node.targets[0], node.value
            elif isinstance(node, ast.AnnAssign):
                target, value = node.target, node.value
            if not (isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name)):
                continue
            if target.value.id != "self":
                continue
            written = _instantiated_class(value)
            qname = resolver.qualify(scope, written) if written else None
            if qname:
                attrs[target.attr] = qname
    return attrs


def collect_function_returns(
    files: list[ParsedFile], module_of: dict[str, str]
) -> dict[str, ast.expr | None]:
    """Kiểu trả về khai báo của mọi hàm và method, tra theo tên đầy đủ."""
    returns: dict[str, ast.expr | None] = {}
    for parsed in files:
        module = module_of[parsed.rel_path]
        prefix = f"{module}." if module else ""
        for node in parsed.tree.body:
            if isinstance(node, FUNCTION_NODES):
                returns[f"{prefix}{node.name}"] = node.returns
            elif isinstance(node, ast.ClassDef):
                for child in node.body:
                    if isinstance(child, FUNCTION_NODES):
                        returns[f"{prefix}{node.name}.{child.name}"] = child.returns
    return returns


def collect_assign_values(
    files: list[ParsedFile], module_of: dict[str, str]
) -> dict[str, tuple[str, ast.expr]]:
    """Giá trị của mọi phép gán ở mức module, dùng để đi theo bí danh kiểu."""
    values: dict[str, tuple[str, ast.expr]] = {}
    for parsed in files:
        module = module_of[parsed.rel_path]
        prefix = f"{module}." if module else ""
        for node in parsed.tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        values[f"{prefix}{target.id}"] = (parsed.rel_path, node.value)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                if node.value is not None:
                    values[f"{prefix}{node.target.id}"] = (parsed.rel_path, node.value)
    return values


def find_external_origin(resolver: Resolver) -> set[str]:
    """Tên nào được gán từ kết quả gọi một thứ ngoài repo.

        log = logging.getLogger(__name__)   -> log đến từ thư viện logging
        SessionLocal = sessionmaker(...)    -> đến từ sqlalchemy
        Base = declarative_base()           -> đến từ sqlalchemy
    """
    external: set[str] = set()
    for qname, (rel_path, value) in resolver.assign_values.items():
        if not isinstance(value, ast.Call):
            continue
        callee = dotted_name(value.func)
        scope = resolver.tables.for_file(rel_path)
        if not callee or scope is None:
            continue
        callee_qname = resolver.qualify(scope, callee)
        if callee_qname and not resolver.index.is_internal(callee_qname):
            external.add(qname)
    return external


def build_resolver(files: list[ParsedFile]) -> tuple[Resolver, dict[str, str]]:
    """Dựng đủ hai bảng tra cứu và mọi thứ cần để nối tham chiếu."""
    index, module_of = build_definition_index(files)
    resolver = Resolver(
        index=index,
        tables=build_import_tables(files, module_of),
        classes=build_class_records(files, module_of),
        function_returns=collect_function_returns(files, module_of),
        assign_values=collect_assign_values(files, module_of),
    )
    resolver.external_origin = find_external_origin(resolver)
    return resolver, module_of


# ---------------------------------------------------------------------------
# Bước 2-4 của mục 15.2: từ một lời gọi ra "hàm nào, file nào"
# ---------------------------------------------------------------------------

def _unresolved(name: str, reason: str) -> Reference:
    """Không tìm được đích. Đây là kết quả hợp lệ (SPEC mục 5.1 quy tắc 6)."""
    return Reference(
        name=name,
        resolved_module=None,
        resolved=False,
        confidence=None,
        completeness="partial",
        reason=reason,
    )


def _resolved(
    name: str,
    rel_path: str,
    symbol: str,
    *,
    inferred: bool = False,
    reason: str | None = None,
) -> Reference:
    return Reference(
        name=name,
        resolved_module=rel_path,
        resolved_symbol=symbol,
        resolved=True,
        confidence="inferred" if inferred else "exact",
        completeness="full",
        reason=reason,
    )


def resolve_call(
    call: ast.Call,
    scope: FileScope,
    var_types: dict[str, str],
    self_attrs: dict[str, str],
    self_class: str | None,
    resolver: Resolver,
) -> Reference | None:
    """Trả lời "lời gọi này trỏ tới đâu". None nghĩa là không đáng ghi nhận.

    Hàm dựng sẵn của Python (print, len, ...) trả về None để tài liệu không bị
    ngập lời gọi vô nghĩa.
    """
    written = dotted_name(call.func)
    if written is None:
        return None

    head, _, tail = written.partition(".")

    if not tail:
        if written in BUILTIN_NAMES and scope.resolve(written) is None:
            return None
        return _resolve_plain_name(written, scope, resolver)

    receiver_class = _receiver_class(head, tail, var_types, self_attrs, self_class, resolver)
    if receiver_class:
        return _resolve_method(written, receiver_class, tail.rpartition(".")[2], resolver)

    return _resolve_via_scope(written, head, tail, scope, resolver)


def _resolve_plain_name(written: str, scope: FileScope, resolver: Resolver) -> Reference:
    """Lời gọi trần: `create_order()` hoặc `OrderService()`."""
    qname = resolver.qualify(scope, written)
    if qname is None:
        if scope.has_wildcard_import:
            return _unresolved(written, "file dùng 'import *', không biết tên này lấy từ đâu")
        return _unresolved(written, f"không tìm thấy khai báo của '{written}' trong repo")

    definition = resolver.index.get(qname)
    if definition:
        return _resolved(written, definition.rel_path, qname)
    if not resolver.index.is_internal(qname):
        return _unresolved(written, f"'{qname}' {EXTERNAL_REASON}")
    return _unresolved(written, f"không tìm thấy khai báo của '{qname}' trong repo")


def _receiver_class(
    head: str,
    tail: str,
    var_types: dict[str, str],
    self_attrs: dict[str, str],
    self_class: str | None,
    resolver: Resolver,
) -> str | None:
    """Đối tượng đứng trước dấu chấm thuộc class nào."""
    if head in var_types:
        return var_types[head]
    if head == "self":
        attr = tail.partition(".")[0]
        if "." in tail and attr in self_attrs:
            return self_attrs[attr]
        if "." not in tail:
            return self_class
    return None


def _resolve_method(written: str, class_qname: str, method: str, resolver: Resolver) -> Reference:
    """Đã biết class, tìm method trong đó rồi leo kế thừa nếu chưa thấy."""
    if class_qname not in resolver.classes:
        if class_qname in resolver.external_origin:
            return _unresolved(written, f"'{class_qname}' là kết quả gọi {EXTERNAL_REASON}")
        if not resolver.index.is_internal(class_qname):
            return _unresolved(written, f"'{class_qname}' {EXTERNAL_REASON}")
        return _unresolved(written, f"không tìm thấy class '{class_qname}' trong repo")

    result = resolver.find_method(class_qname, method)
    if result.owner is None:
        if result.stopped_at_external_base:
            return _unresolved(written, f"{result.reason} — {EXTERNAL_REASON}")
        return _unresolved(written, result.reason or "không tìm thấy method")

    definition = resolver.index.method_of(result.owner.qualified_name, method)
    rel_path = definition.rel_path if definition else result.owner.rel_path
    symbol = f"{result.owner.qualified_name}.{method}"
    return _resolved(written, rel_path, symbol, inferred=result.ambiguous, reason=result.reason)


def _resolve_via_scope(
    written: str, head: str, tail: str, scope: FileScope, resolver: Resolver
) -> Reference:
    """`httpx.post()` hoặc `order_service.create()` — đầu là module hay class."""
    head_qname = scope.resolve(head)
    if head_qname is None:
        if scope.has_wildcard_import:
            return _unresolved(written, "file dùng 'import *', không biết tên này lấy từ đâu")
        return _unresolved(written, f"không biết '{head}' là gì trong file này")

    if head_qname in resolver.external_origin:
        return _unresolved(written, f"'{head_qname}' là kết quả gọi {EXTERNAL_REASON}")

    if not resolver.index.is_internal(head_qname):
        return _unresolved(written, f"'{head_qname}' {EXTERNAL_REASON}")

    if head_qname in resolver.classes:
        return _resolve_method(written, head_qname, tail.rpartition(".")[2], resolver)

    full = f"{head_qname}.{tail}"
    definition = resolver.index.get(full)
    if definition:
        return _resolved(written, definition.rel_path, full)
    if full in resolver.classes:
        return _resolved(written, resolver.classes[full].rel_path, full)
    return _unresolved(written, f"không tìm thấy khai báo của '{full}' trong repo")
