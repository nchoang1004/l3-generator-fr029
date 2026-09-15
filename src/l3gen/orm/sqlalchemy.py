"""Tìm bảng cơ sở dữ liệu khai báo bằng SQLAlchemy hoặc SQLModel (bước 3b).

Câu hỏi cốt lõi: `class Order(Base)` — `Base` này có phải của SQLAlchemy không?
Cây cú pháp chỉ thấy chữ "Base". Phải tra bảng tên gọi của file, rồi xem giá trị
gán cho nó có phải `declarative_base()` hay không.

Nhận ba kiểu khai báo:
    class Order(Base)                   Base = declarative_base()      (SQLAlchemy 1.x)
    class Order(DeclarativeBase)        kế thừa thẳng                  (SQLAlchemy 2.0)
    class Order(SQLModel, table=True)   SQLModel dựng trên SQLAlchemy
"""

import ast
from dataclasses import dataclass

from l3gen.languages.python.literals import is_true, keyword_of, read_text
from l3gen.languages.python.parser import ParsedFile
from l3gen.languages.python.resolution import FUNCTION_NODES, Resolver, dotted_name
from l3gen.models.iam import DBColumn, DBEntity, Reference, SourceLocation

DECLARATIVE_FACTORY = "declarative_base"
DECLARATIVE_BASES = ("DeclarativeBase", "DeclarativeBaseNoMeta")
COLUMN_FACTORIES = ("Column", "mapped_column")
SQLMODEL_FIELD = "Field"
RELATIONSHIP_FACTORIES = ("Relationship", "relationship")
MAX_BASE_DEPTH = 10


@dataclass
class ClassNode:
    """Một class kèm cây cú pháp của nó, để đọc thân class."""

    qualified_name: str
    rel_path: str
    node: ast.ClassDef


def collect_class_nodes(
    files: list[ParsedFile], module_of: dict[str, str]
) -> dict[str, ClassNode]:
    nodes: dict[str, ClassNode] = {}
    for parsed in files:
        module = module_of[parsed.rel_path]
        prefix = f"{module}." if module else ""
        for node in parsed.tree.body:
            if isinstance(node, ast.ClassDef):
                qname = f"{prefix}{node.name}"
                nodes[qname] = ClassNode(qname, parsed.rel_path, node)
    return nodes


def _is_declarative_base(qname: str, resolver: Resolver) -> bool:
    """Tên này có được gán bằng `declarative_base()` không."""
    entry = resolver.assign_values.get(qname)
    if entry is None:
        return False
    _, value = entry
    if not isinstance(value, ast.Call):
        return False
    callee = dotted_name(value.func)
    return bool(callee) and callee.split(".")[-1] == DECLARATIVE_FACTORY


def find_orm_base(
    cls: ClassNode, classes: dict[str, ClassNode], resolver: Resolver
) -> tuple[str, str] | None:
    """Đi ngược cây kế thừa tìm gốc SQLAlchemy.

    Trả về (tên đầy đủ của class cha trực tiếp, kiểu ORM) hoặc None.
    Xử lý được ca class trung gian ở file khác — đây chính là fixture 7.
    """
    if any(kw.arg == "table" and is_true(kw.value) for kw in cls.node.keywords):
        return _direct_base(cls, resolver), "sqlmodel"

    visited: set[str] = set()
    level = [cls]

    for _ in range(MAX_BASE_DEPTH):
        parents: list[ClassNode] = []
        for child in level:
            scope = resolver.tables.for_file(child.rel_path)
            if scope is None:
                continue
            for base in child.node.bases:
                written = dotted_name(base)
                if not written:
                    continue
                base_qname = resolver.qualify(scope, written)
                if base_qname is None:
                    continue
                if _is_declarative_base(base_qname, resolver):
                    return _direct_base(cls, resolver), "sqlalchemy"
                if base_qname.split(".")[-1] in DECLARATIVE_BASES:
                    return _direct_base(cls, resolver), "sqlalchemy"
                if base_qname in classes and base_qname not in visited:
                    visited.add(base_qname)
                    parents.append(classes[base_qname])
        if not parents:
            return None
        level = parents
    return None


def _direct_base(cls: ClassNode, resolver: Resolver) -> str | None:
    scope = resolver.tables.for_file(cls.rel_path)
    for base in cls.node.bases:
        written = dotted_name(base)
        if written and scope is not None:
            return resolver.qualify(scope, written) or written
    return None


def _base_reference(base_qname: str | None, resolver: Resolver) -> Reference | None:
    if base_qname is None:
        return None
    definition = resolver.index.get(base_qname)
    if definition is not None:
        return Reference(
            name=base_qname.split(".")[-1],
            resolved_module=definition.rel_path,
            resolved=True,
            confidence="exact",
            completeness="full",
            reason=None,
        )
    return Reference(
        name=base_qname.split(".")[-1],
        resolved_module=None,
        resolved=False,
        confidence=None,
        completeness="partial",
        reason=f"'{base_qname}' thuộc thư viện ngoài, ngoài phạm vi repo",
    )


def _column_from_call(name: str, call: ast.Call) -> DBColumn | None:
    """Đọc `Column(Integer, ForeignKey("customers.id"), primary_key=True)`."""
    factory = dotted_name(call.func)
    if not factory or factory.split(".")[-1] not in COLUMN_FACTORIES:
        return None

    col_type = "?"
    foreign_key = None
    for arg in call.args:
        inner = dotted_name(arg.func) if isinstance(arg, ast.Call) else None
        if inner and inner.split(".")[-1] == "ForeignKey":
            target = read_text(arg.args[0]) if arg.args else None
            foreign_key = target.text if target else None
        elif col_type == "?":
            col_type = ast.unparse(arg)

    fk_keyword = keyword_of(call, "foreign_key")
    if foreign_key is None and fk_keyword is not None:
        target = read_text(fk_keyword)
        foreign_key = target.text if target else None

    return DBColumn(
        name=name,
        type=col_type,
        is_primary_key=is_true(keyword_of(call, "primary_key")),
        foreign_key_ref=foreign_key,
    )


def _column_from_annotation(name: str, node: ast.AnnAssign) -> DBColumn:
    """Đọc `id: int | None = Field(primary_key=True)` kiểu SQLModel / Mapped."""
    declared = ast.unparse(node.annotation)
    if declared.startswith("Mapped[") and declared.endswith("]"):
        declared = declared[len("Mapped[") : -1]

    primary_key = False
    foreign_key = None
    if isinstance(node.value, ast.Call):
        factory = dotted_name(node.value.func)
        if factory and factory.split(".")[-1] in (*COLUMN_FACTORIES, SQLMODEL_FIELD):
            primary_key = is_true(keyword_of(node.value, "primary_key"))
            fk = keyword_of(node.value, "foreign_key")
            target = read_text(fk) if fk is not None else None
            foreign_key = target.text if target else None

    return DBColumn(
        name=name, type=declared, is_primary_key=primary_key, foreign_key_ref=foreign_key
    )


def _is_relationship(value: ast.expr | None) -> bool:
    """`owner: User | None = Relationship(...)` là quan hệ giữa hai bảng, không phải cột."""
    if not isinstance(value, ast.Call):
        return False
    factory = dotted_name(value.func)
    return bool(factory) and factory.split(".")[-1] in RELATIONSHIP_FACTORIES


def is_abstract(class_node: ast.ClassDef) -> bool:
    """`__abstract__ = True` nghĩa là class trung gian, không phải bảng thật."""
    for member in class_node.body:
        if not isinstance(member, ast.Assign):
            continue
        for target in member.targets:
            if isinstance(target, ast.Name) and target.id == "__abstract__":
                return is_true(member.value)
    return False


def read_columns(class_node: ast.ClassDef) -> list[DBColumn]:
    columns: list[DBColumn] = []
    for member in class_node.body:
        if isinstance(member, ast.AnnAssign) and isinstance(member.target, ast.Name):
            if member.target.id.startswith("__") or _is_relationship(member.value):
                continue
            columns.append(_column_from_annotation(member.target.id, member))
        elif isinstance(member, ast.Assign) and isinstance(member.value, ast.Call):
            for target in member.targets:
                if not isinstance(target, ast.Name) or target.id.startswith("__"):
                    continue
                column = _column_from_call(target.id, member.value)
                if column is not None:
                    columns.append(column)
    return columns


def read_table_name(class_node: ast.ClassDef, orm: str) -> tuple[str | None, str, str, str | None]:
    """Trả về (tên bảng, confidence, completeness, reason).

    Tên bảng là None khi không đọc được — xem docstring của `DBEntity.table_name`.
    """
    for member in class_node.body:
        if not isinstance(member, ast.Assign):
            continue
        for target in member.targets:
            if isinstance(target, ast.Name) and target.id == "__tablename__":
                value = read_text(member.value)
                if value is None:
                    break
                if value.is_literal:
                    return value.text, "exact", "full", None
                return (
                    value.text,
                    "exact",
                    "partial",
                    f"__tablename__ ghép từ biến, chưa giải được giá trị: {value.text}",
                )

    if orm == "sqlmodel":
        # SQLModel có quy tắc mặc định tường minh: __tablename__ = tên class viết
        # thường. Đây là đọc quy tắc của thư viện, không phải đoán.
        return (
            class_node.name.lower(),
            "inferred",
            "full",
            "không khai báo __tablename__; SQLModel lấy mặc định là tên class viết thường",
        )
    # SQLAlchemy thuần KHÔNG tự sinh __tablename__. Lớp nào thiếu mà vẫn chạy được
    # thì lớp cơ sở của repo đó có declared_attr sinh tên lúc chạy — mỗi repo một
    # quy tắc riêng, không đọc được bằng phân tích cú pháp. Ghi None còn hơn đoán:
    # trên Netflix/dispatch quy ước "tên class viết thường" sai 7/9 ca.
    return (
        None,
        "exact",
        "partial",
        "không khai báo __tablename__; tên bảng do lớp cơ sở sinh lúc chạy, "
        "không đọc được bằng phân tích cú pháp",
    )


def extract_entities(
    files: list[ParsedFile], resolver: Resolver, module_of: dict[str, str], service: str
) -> list[DBEntity]:
    classes = collect_class_nodes(files, module_of)
    entities: list[DBEntity] = []

    for qname, cls in classes.items():
        found = find_orm_base(cls, classes, resolver)
        if found is None or is_abstract(cls.node):
            continue
        base_qname, orm = found
        table_name, confidence, completeness, reason = read_table_name(cls.node, orm)

        entities.append(
            DBEntity(
                service=service,
                class_name=cls.node.name,
                table_name=table_name,
                columns=read_columns(cls.node),
                base_class=_base_reference(base_qname, resolver),
                confidence=confidence,
                completeness=completeness,
                reason=reason,
                location=SourceLocation(
                    file=cls.rel_path,
                    line_start=cls.node.lineno,
                    line_end=getattr(cls.node, "end_lineno", cls.node.lineno) or cls.node.lineno,
                ),
            )
        )

    entities.sort(key=lambda e: (e.table_name or "", e.location.file, e.location.line_start))
    return entities
