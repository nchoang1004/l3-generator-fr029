"""Phần bảng CSDL (FR-030), lỗi tìm khi đo với golden v1 ngày 12/10/2026 (32 bảng, 341 cột trên 4 repo):
khóa chính khai qua alias Annotated, bảng mở rộng bằng lớp con cùng __tablename__, và AC-030-04 (ORM khác, bảng chỉ
có trong migration, SQL viết tay phải ghi ở phần giới hạn, không được coi là repo không có bảng)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE)]

from l3slice import snapshot  # noqa: E402
from l3slice.docstatic import static_facts  # noqa: E402
from l3slice.source_tools import SourceTools  # noqa: E402


def static_of(files: dict):
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        for rel, text in files.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(text, encoding="utf-8")
        snap, sources = snapshot.take(root)
        tools = SourceTools(snap, sources)
        facts, limits, _ = static_facts(snap, sources, tools, snapshot.inventory(snap)["units"][0]["id"])
    return [f for f in facts if f["kind"] == "table"], limits


def column(table, name):
    return next(c for c in table["attributes"]["columns"]["value"] if c["name"]["value"] == name)


BASE = ("from typing import Annotated\nfrom sqlalchemy import BigInteger\n"
        "from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column\n\nAUTO = True\n\n"
        "id_key = Annotated[\n    int,\n    mapped_column(BigInteger, primary_key=True)\n"
        "    if AUTO\n    else mapped_column(BigInteger, primary_key=True, default=1),\n]\n\n\n"
        "class Base(DeclarativeBase):\n    pass\n")


class AliasPrimaryKey(unittest.TestCase):
    def test_primary_key_from_an_annotated_alias_is_read(self):
        model = ('from sqlalchemy.orm import Mapped, mapped_column\nfrom base import Base, id_key\n\n\n'
                 'class Config(Base):\n    __tablename__ = "sys_config"\n    id: Mapped[id_key] = mapped_column(init=False)\n'
                 '    name: Mapped[str] = mapped_column()\n')
        [t], _ = static_of({"base.py": BASE, "config.py": model})
        pk = column(t, "id")
        self.assertEqual((pk["primary_key"]["state"], pk["primary_key"]["value"]), ("known", True))
        self.assertEqual(pk["nullable"]["value"], False)
        self.assertEqual(column(t, "name")["primary_key"]["value"], False)

    def test_branches_that_disagree_leave_it_unknown(self):
        base = BASE.replace("primary_key=True, default=1", "primary_key=False, default=1")
        model = ('from sqlalchemy.orm import Mapped, mapped_column\nfrom base import Base, id_key\n\n\n'
                 'class Config(Base):\n    __tablename__ = "sys_config"\n    id: Mapped[id_key] = mapped_column(init=False)\n')
        [t], _ = static_of({"base.py": base, "config.py": model})
        self.assertEqual(column(t, "id")["primary_key"]["state"], "unknown")


class ExtendedTable(unittest.TestCase):
    def test_a_subclass_with_the_same_table_name_is_one_table_with_all_columns(self):
        model = ("import sqlalchemy as sa\nfrom sqlalchemy.orm import declarative_base\nBase = declarative_base()\n\n\n"
                 "class Task(Base):\n    __tablename__ = 'task_result'\n    id = sa.Column(sa.Integer, primary_key=True)\n"
                 "    status = sa.Column(sa.String(64))\n\n\nclass TaskExtended(Task):\n    __tablename__ = 'task_result'\n"
                 "    __table_args__ = {'extend_existing': True}\n    name = sa.Column(sa.String(155), nullable=True)\n")
        tables, _ = static_of({"result.py": model})
        self.assertEqual(len(tables), 1)
        self.assertEqual([c["name"]["value"] for c in tables[0]["attributes"]["columns"]["value"]], ["id", "status", "name"])


class Unsupported(unittest.TestCase):
    def codes(self, files):
        return {x["code"]: x["message"] for x in static_of(files)[1]}

    def test_other_orms_are_named_with_their_place(self):
        tortoise = ("from tortoise import fields, models\n\n\nclass TextSummary(models.Model):\n"
                    "    url = fields.TextField()\n")
        msg = self.codes({"app/models.py": tortoise}).get("TABLES_NOT_READ", "")
        self.assertIn("Tortoise", msg)
        self.assertIn("app/models.py:4", msg)

    def test_tables_only_in_migrations_are_named(self):
        mig = ("from alembic import op\nimport sqlalchemy as sa\n\n\ndef upgrade():\n"
               "    op.create_table('orders', sa.Column('id', sa.Integer(), primary_key=True))\n")
        msg = self.codes({"app/main.py": "x = 1\n", "migrations/versions/001_init.py": mig}).get("TABLES_NOT_READ", "")
        self.assertIn("migration", msg)
        self.assertIn("orders", msg)

    def test_hand_written_sql_is_named(self):
        sql = 'import sqlite3\n\nDDL = """CREATE TABLE items (id INTEGER PRIMARY KEY)"""\n'
        self.assertIn("app/db.py:3", self.codes({"app/db.py": sql}).get("TABLES_NOT_READ", ""))

    def test_a_sqlalchemy_repo_gets_no_such_note(self):
        model = ("import sqlalchemy as sa\nfrom sqlalchemy.orm import declarative_base\nBase = declarative_base()\n\n\n"
                 "class T(Base):\n    __tablename__ = 't'\n    id = sa.Column(sa.Integer, primary_key=True)\n")
        self.assertNotIn("TABLES_NOT_READ", self.codes({"app/m.py": model}))


class JudgeFindings(unittest.TestCase):
    """Giám khảo độc lập chấm phần CSDL (12/10/2026): ràng buộc từ alias, ondelete của SQLModel, ràng buộc nhiều cột
    trong __table_args__, CREATE TABLE trong migration, nhãn không nói trường nào là suy luận."""

    def test_unique_and_index_come_through_the_alias(self):
        base = BASE.replace("mapped_column(BigInteger, primary_key=True)\n",
                            "mapped_column(BigInteger, primary_key=True, unique=True, index=True)\n").replace(
            "primary_key=True, default=1", "primary_key=True, unique=True, index=True, default=1")
        model = ('from sqlalchemy.orm import Mapped, mapped_column\nfrom base import Base, id_key\n\n\n'
                 'class Config(Base):\n    __tablename__ = "sys_config"\n    id: Mapped[id_key] = mapped_column(init=False)\n')
        [t], _ = static_of({"base.py": base, "config.py": model})
        self.assertEqual(column(t, "id")["constraints"]["value"], ["unique", "index"])

    def test_sqlmodel_on_delete_is_read(self):
        model = ("import uuid\nfrom sqlmodel import Field, SQLModel\n\n\nclass Item(SQLModel, table=True):\n"
                 "    id: uuid.UUID = Field(primary_key=True)\n"
                 "    owner_id: uuid.UUID = Field(foreign_key='user.id', nullable=False, ondelete='CASCADE')\n")
        [t], _ = static_of({"models.py": model})
        self.assertEqual(column(t, "owner_id")["foreign_key"]["value"], {"table": "user", "column": "id", "ondelete": "CASCADE"})

    def test_multi_column_constraints_of_table_args(self):
        model = ("import sqlalchemy as sa\nfrom sqlalchemy.orm import declarative_base\nBase = declarative_base()\n\n\n"
                 "class Rule(Base):\n    __tablename__ = 'sys_rule'\n"
                 "    __table_args__ = (sa.UniqueConstraint('name', 'deleted', name='uk_rule'), sa.Index('ix_rule', 'name'))\n"
                 "    id = sa.Column(sa.Integer, primary_key=True)\n    name = sa.Column(sa.String)\n")
        [t], _ = static_of({"m.py": model})
        self.assertEqual(t["attributes"]["table_constraints"]["value"], ["unique(name, deleted) uk_rule", "index(name) ix_rule"])

    def test_create_table_in_a_migration_is_named(self):
        mig = ('from tortoise import BaseDBAsyncClient\n\n\nasync def upgrade(db: BaseDBAsyncClient) -> str:\n'
               '    return """\n        CREATE TABLE IF NOT EXISTS "textsummary" (\n    "id" SERIAL NOT NULL PRIMARY KEY\n);"""\n')
        _, limits = static_of({"app/main.py": "x = 1\n", "migrations/models/0_init.py": mig})
        self.assertIn("textsummary", next(x["message"] for x in limits if x["code"] == "TABLES_NOT_READ"))

    def test_the_label_names_the_inferred_fields(self):
        model = ("import sqlalchemy as sa\nfrom sqlalchemy.orm import declarative_base\nBase = declarative_base()\n\n\n"
                 "class T(Base):\n    __tablename__ = 't'\n    id = sa.Column(sa.Integer, primary_key=True, nullable=False)\n"
                 "    note = sa.Column(sa.String)\n")
        [t], _ = static_of({"m.py": model})
        self.assertNotIn("inferred_fields", column(t, "id"))  # both written in code
        self.assertEqual(column(t, "note")["inferred_fields"]["value"], ["primary_key", "nullable"])


class JudgeRoundTwo(unittest.TestCase):
    """Giám khảo vòng 2 (12/10/2026): sa_type của SQLModel bị bỏ qua (ghi datetime thay DateTime(timezone=True)),
    max_length không được ghi, khóa chính ghép của bảng nối không được nói rõ."""

    SQLMODEL = ("from datetime import datetime\nfrom sqlalchemy import DateTime\nfrom sqlmodel import Field, SQLModel\n\n\n"
                "class Item(SQLModel, table=True):\n    id: int = Field(primary_key=True)\n"
                "    title: str = Field(max_length=255)\n"
                "    created_at: datetime | None = Field(default=None, sa_type=DateTime(timezone=True))\n")

    def test_sa_type_and_max_length_are_the_declared_type(self):
        [t], _ = static_of({"models.py": self.SQLMODEL})
        self.assertIn("khai trong code: DateTime(timezone=True)", column(t, "created_at")["type"]["reason"])
        self.assertIn("khai trong code: str, max_length=255", column(t, "title")["type"]["reason"])

    def test_composite_primary_key_is_named(self):
        import json as _json
        from l3slice.docagent import ScriptedProvider
        from l3slice.docpipeline import run_documents
        src = ("import sqlalchemy as sa\nfrom sqlalchemy.orm import declarative_base\nBase = declarative_base()\n\n\n"
               "user_role = sa.Table('sys_user_role', Base.metadata,\n"
               "    sa.Column('user_id', sa.Integer, primary_key=True),\n    sa.Column('role_id', sa.Integer, primary_key=True))\n")
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "src").mkdir()
            (root / "src/m2m.py").write_text(src, encoding="utf-8")
            (root / "m.json").write_text(_json.dumps({"components": [{"name": "Data", "files": ["m2m.py"]}]}), encoding="utf-8")
            run_documents(root / "src", root / "out", root / "m.json", "demo", ScriptedProvider([]))
            doc = (root / "out/TAI-LIEU.md").read_text(encoding="utf-8")
        self.assertIn("Khóa chính ghép: user_id, role_id.", doc)


MODELS = ("import sqlalchemy as sa\nfrom sqlalchemy.orm import declarative_base\nBase = declarative_base()\n\n\n"
          "class Order(Base):\n    __tablename__ = 'orders'\n    id = sa.Column(sa.Integer, primary_key=True)\n\n\n"
          "class OrderItem(Base):\n    __tablename__ = 'order_items'\n    id = sa.Column(sa.Integer, primary_key=True)\n"
          "    order_id = sa.Column(sa.Integer, sa.ForeignKey('orders.id'), nullable=False)\n    note = sa.Column(sa.String)\n"
          "    sku = sa.Column(sa.String(64), unique=True, index=True)\n"
          "    parent_id = sa.Column(sa.Integer, sa.ForeignKey('orders.id', ondelete='CASCADE'))\n\n\n"
          "order_tags = sa.Table('order_tags', Base.metadata, sa.Column('order_id', sa.Integer, primary_key=True))\n")


class Presentation(unittest.TestCase):
    """FR-030 'Mỗi bảng: tên bảng, lớp model và vị trí khai báo'; 'Truy vết: file:dòng của từng bảng và cột';
    AC-030-01: mỗi dòng mang nhãn exact / inferred kèm quy tắc / unknown. API-008 §6: mỗi cột có bằng chứng."""

    @classmethod
    def setUpClass(cls):
        import json as _json
        from l3slice.docagent import ScriptedProvider
        from l3slice.docpipeline import run_documents
        cls.t = tempfile.TemporaryDirectory()
        root = Path(cls.t.name)
        (root / "src").mkdir()
        (root / "src/models.py").write_text(MODELS, encoding="utf-8")
        (root / "src/main.py").write_text("x = 1\n", encoding="utf-8")
        (root / "m.json").write_text(_json.dumps({"components": [{"name": "Data", "files": ["models.py", "main.py"]}]}),
                                     encoding="utf-8")
        cls.bundle = run_documents(root / "src", root / "out", root / "m.json", "demo", ScriptedProvider([]))
        cls.tbl = (root / "out/tech-specs/DATA/schema/TBL-DEMO-DATA.md").read_text(encoding="utf-8")
        cls.doc = (root / "out/TAI-LIEU.md").read_text(encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.t.cleanup()

    def test_tbl_names_the_model_class_and_its_line(self):
        art = next(a for a in self.bundle["artifacts"] if a["kind"] == "table")
        self.assertEqual(art["status"], "ready", art.get("error"))
        self.assertIn("Lớp model `OrderItem`, khai ở `models.py:11`", self.tbl)

    def test_every_column_row_has_label_and_evidence(self):
        # the label says which values come from a default, by which rule (judge 12/10: "exact" was never visible)
        self.assertIn("| order_id | unknown — Chưa xác định SQL dialect từ source; khai trong code: sa.Integer | không | "
                      "orders.id | không | inferred: primary_key (sqlalchemy-defaults-v1); unknown: type | `models.py:14` |",
                      self.tbl)
        self.assertIn("| id | unknown — Chưa xác định SQL dialect từ source; khai trong code: sa.Integer | có | — | không | "
                      "inferred: nullable (sqlalchemy-defaults-v1); unknown: type | `models.py:13` |", self.tbl)
        self.assertNotIn('{"column"', self.tbl)

    def test_tai_lieu_has_an_overview_of_tables(self):
        section = self.doc.split("\n## 4.")[1].split("\n## 5.")[0]
        self.assertIn("Mọi bảng thuộc component Data.", section)  # one component: no column for it
        self.assertIn("| Bảng | Lớp model | Số cột | Khóa ngoại tới |", section)
        self.assertIn("| order_items | OrderItem | 5 | orders |", section)
        self.assertIn("| order_tags | `order_tags = Table(...)` | 1 | — |", section)  # not "chưa rõ"
        self.assertIn("Khai bằng `order_tags = Table(...)` ở `models.py:20`", self.tbl)
        self.assertIn("Lớp `OrderItem`, khai ở `models.py:11`", section)

    def test_tai_lieu_says_the_dialect_once_and_shows_constraints(self):
        section = self.doc.split("\n## 4.")[1].split("\n## 5.")[0]
        self.assertEqual(section.count("SQL dialect"), 1)
        self.assertNotIn("chưa quy ra kiểu SQL)", section.split("| Cột |")[1])  # explained once, not per column
        self.assertIn("| sku | sa.String(64) | không\\* | — | có\\* | unique, index |", section)  # * = ORM default
        self.assertIn("| parent_id | sa.Integer | không\\* | orders.id | có\\* | xóa theo: CASCADE |", section)
        self.assertIn("| id | sa.Integer | có | — | không\\* | — |", section)
        self.assertNotIn("sqlalchemy-defaults-v1", section)  # column defaults are the *, not a note with a rule id
        self.assertNotIn("Suy luận:", section)


if __name__ == "__main__":
    unittest.main()
