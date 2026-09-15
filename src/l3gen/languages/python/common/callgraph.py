"""Duyệt mọi hàm trong repo và nối từng lời gọi bên trong (bước 3d).

Dùng chung cho mọi framework Python — FastAPI, Flask hay script thuần đều giống
nhau ở chỗ này.
"""

import ast

from l3gen.languages.python.parser import ParsedFile
from l3gen.languages.python.resolution import (
    FUNCTION_NODES,
    Resolver,
    infer_self_attributes,
    infer_variable_types,
    resolve_call,
)
from l3gen.models.iam import FunctionNode, Reference, SourceLocation


def extract_functions(
    files: list[ParsedFile],
    resolver: Resolver,
    module_of: dict[str, str],
    service: str,
    entity_classes: frozenset[str] = frozenset(),
) -> list[FunctionNode]:
    """Mỗi hàm và mỗi method thành một FunctionNode, kèm các lời gọi đã nối.

    entity_classes là tên đầy đủ của các class bảng dữ liệu. Hàm nào nhắc tới một
    trong số đó thì ghi vào entity_refs — đây là dữ liệu để nối route xuống bảng.
    """
    nodes: list[FunctionNode] = []

    for parsed in files:
        scope = resolver.tables.for_file(parsed.rel_path)
        if scope is None:
            continue
        module = module_of[parsed.rel_path]
        prefix = f"{module}." if module else ""

        for node in parsed.tree.body:
            if isinstance(node, FUNCTION_NODES):
                nodes.append(
                    _build(
                        node, f"{prefix}{node.name}", parsed.rel_path, None, None,
                        {}, scope, resolver, service, entity_classes,
                    )
                )
            elif isinstance(node, ast.ClassDef):
                class_qname = f"{prefix}{node.name}"
                self_attrs = infer_self_attributes(node, scope, resolver)
                for child in node.body:
                    if isinstance(child, FUNCTION_NODES):
                        nodes.append(
                            _build(
                                child, f"{class_qname}.{child.name}", parsed.rel_path,
                                node.name, class_qname, self_attrs, scope, resolver, service,
                                entity_classes,
                            )
                        )
    return nodes


def _build(
    func, qualified_name, rel_path, class_name, class_qname, self_attrs, scope, resolver,
    service, entity_classes=frozenset()
) -> FunctionNode:
    return FunctionNode(
        service=service,
        qualified_name=qualified_name,
        name=func.name,
        class_name=class_name,
        module=rel_path,
        calls=calls_inside(func, scope, resolver, self_attrs, class_qname),
        entity_refs=entities_inside(func, scope, resolver, entity_classes),
        location=SourceLocation(
            file=rel_path,
            line_start=func.lineno,
            line_end=getattr(func, "end_lineno", func.lineno) or func.lineno,
        ),
    )


def calls_inside(
    func,
    scope,
    resolver: Resolver,
    self_attrs: dict[str, str] | None = None,
    class_qname: str | None = None,
) -> list[Reference]:
    """Mọi lời gọi bên trong một hàm, đã cố nối tới đích.

    Chỉ duyệt THÂN hàm. Decorator và giá trị mặc định của tham số nằm ngoài thân,
    không phải lời gọi khi hàm chạy — `@router.post(...)` là khai báo route, còn
    `Depends(...)` là khai báo phụ thuộc. Hai thứ đó do bộ trích xuất riêng lo.

    Hàm lồng bên trong được tính chung vào hàm ngoài — chấp nhận được vì tài liệu
    L3 quan tâm "hàm này chạm tới cái gì", không quan tâm lồng mấy tầng.
    """
    var_types = infer_variable_types(func, scope, resolver)
    seen: set[str] = set()
    refs: list[Reference] = []

    for statement in func.body:
        for node in ast.walk(statement):
            if not isinstance(node, ast.Call):
                continue
            ref = resolve_call(
                node, scope, var_types, self_attrs or {}, class_qname, resolver
            )
            if ref is None or ref.name in seen:
                continue
            seen.add(ref.name)
            refs.append(ref)

    return refs


def entities_inside(func, scope, resolver: Resolver, entity_classes: frozenset[str]):
    """Các class bảng dữ liệu mà hàm này nhắc tới.

    `db.query(Order)` — `Order` là một tên trần, không phải lời gọi, nên phần nối
    lời gọi ở trên bỏ qua nó. Nhưng đây chính là chỗ cho biết route nào đọc bảng
    nào, nên phải bắt riêng.
    """
    if not entity_classes:
        return []

    found: dict[str, Reference] = {}
    for statement in func.body:
        for node in ast.walk(statement):
            if not isinstance(node, ast.Name):
                continue
            qname = scope.resolve(node.id)
            if qname in entity_classes and qname not in found:
                definition = resolver.index.get(qname)
                found[qname] = Reference(
                    name=node.id,
                    resolved_module=definition.rel_path if definition else None,
                    resolved_symbol=qname,
                    resolved=definition is not None,
                    confidence="exact" if definition else None,
                    completeness="full" if definition else "partial",
                    reason=None if definition else f"không tìm thấy '{qname}' trong repo",
                )
    return list(found.values())
