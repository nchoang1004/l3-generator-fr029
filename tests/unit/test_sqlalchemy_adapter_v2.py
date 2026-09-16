"""SQLAlchemy V2 adapter dùng IR chung và full symbol đã resolve."""

import ast

from l3gen.core.resolution.dataflow import resolve_program
from l3gen.languages.python.frontend import build_semantic_program
from l3gen.languages.python.parser import ParsedFile
from l3gen.orm.sqlalchemy_v2 import extract_entities_v2


def entities(files: dict[str, str]):
    parsed = [
        ParsedFile(path, ast.parse(source), source.count("\n") + 1)
        for path, source in files.items()
    ]
    modules = {path: path.removesuffix(".py").replace("/", ".") for path in files}
    program = build_semantic_program(parsed, modules)
    return extract_entities_v2(program, resolve_program(program))


def test_declarative_base_column_foreign_key_va_abstract_class():
    result = entities(
        {
            "models.py": """
from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from sqlalchemy import ForeignKey
Base = declarative_base()

class Common(Base):
    __abstract__ = True

class Order(Common):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
"""
        }
    )

    assert len(result) == 1
    assert result[0].class_name == "Order"
    assert result[0].table_name == "orders"
    assert [(column.name, column.type) for column in result[0].columns] == [
        ("id", "int"),
        ("owner_id", "int"),
    ]
    assert result[0].columns[1].foreign_key_ref == "users.id"


def test_sqlmodel_table_true_va_relationship_khong_bi_tinh_la_column():
    result = entities(
        {
            "models.py": """
from sqlmodel import SQLModel, Field, Relationship
class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    groups: list["Group"] = Relationship()
"""
        }
    )

    assert len(result) == 1
    assert result[0].table_name == "user"
    assert [column.name for column in result[0].columns] == ["id"]


def test_lop_trung_gian_o_file_khac_van_noi_duoc_ve_base():
    result = entities(
        {
            "base.py": """
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase): pass
""",
            "models.py": """
from base import Base
class Order(Base):
    __tablename__ = "orders"
""",
        }
    )

    assert [item.class_name for item in result] == ["Order"]
    assert result[0].base_class.resolved_symbol == "base.Base"

