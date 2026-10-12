"""Đợt 1: extractor (CMP-004) on small inline sources. Every FactSet is validated against API-004."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import contracts  # noqa: E402
from l3slice import extract, snapshot  # noqa: E402


def facts_of(files: dict[str, str]):
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        for rel, text in files.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(text, encoding="utf-8")
        snap, sources = snapshot.take(root)
        fs = extract.extract(snap, sources, snapshot.inventory(snap)["units"][0]["id"])
    contracts.validate(fs, 4, "FactSet")
    return fs


def kind(fs, k):
    return [f for f in fs["facts"] if f["kind"] == k]


def val(f, name):
    v = f["attributes"].get(name)
    return v["value"] if v and v["state"] == "known" else (None if v is None else v["state"])


ROUTER = 'from fastapi import APIRouter\nrouter = APIRouter(prefix="/orders")\n\n@router.post("/{order_id}/confirm", status_code=201)\ndef confirm(order_id: int):\n    return {}\n'


class Routes(unittest.TestCase):
    def test_include_router_prefix_chain(self):
        fs = facts_of({"routes.py": ROUTER, "main.py": "from fastapi import FastAPI\nfrom routes import router\n"
                       "app = FastAPI()\napp.include_router(router, prefix='/api/v1')\n"})
        [r] = kind(fs, "route")
        self.assertEqual(val(r, "path"), "/api/v1/orders/{order_id}/confirm")
        self.assertEqual(val(r, "registration_context"), "main.py::app->routes.py::router")
        self.assertEqual(val(r, "status_codes"), [201])
        [p] = val(r, "parameters")
        self.assertEqual((p["name"]["value"], p["in"]["value"], p["required"]["value"]), ("order_id", "path", True))

    def test_two_apps_give_two_registrations(self):
        fs = facts_of({"routes.py": ROUTER, "main.py": "from fastapi import FastAPI\nfrom routes import router\n"
                       "a = FastAPI()\nb = FastAPI()\na.include_router(router)\nb.include_router(router)\n"})
        self.assertEqual(sorted(val(r, "application_id") for r in kind(fs, "route")), ["app:main.py::a", "app:main.py::b"])

    def test_mount_and_condition(self):
        fs = facts_of({"routes.py": ROUTER, "main.py": "import os\nfrom fastapi import FastAPI\nfrom routes import router\n"
                       "app = FastAPI()\napi = FastAPI()\nif os.environ.get('ON') == '1':\n    api.include_router(router)\n"
                       "app.mount('/api', api)\n"})
        [r] = kind(fs, "route")
        self.assertEqual(val(r, "path"), "/api/orders/{order_id}/confirm")
        self.assertEqual(val(r, "registration_context"), "main.py::app->main.py::api->routes.py::router")
        self.assertEqual(val(r, "condition"), "os.environ.get('ON') == '1'")

    def test_app_factory_and_wrapper_arguments(self):
        fs = facts_of({"routes.py": ROUTER,
                       "reg.py": "def attach(app, router, prefix):\n    app.include_router(router, prefix=prefix)\n",
                       "main.py": "from fastapi import FastAPI\nfrom routes import router\nfrom reg import attach\n"
                                  "def create_app():\n    app = FastAPI()\n    attach(app, router, prefix='/v2')\n    return app\n"})
        [r] = kind(fs, "route")
        self.assertEqual(val(r, "registration_context"), "main.py::create_app.app->routes.py::router")
        self.assertEqual(val(r, "path"), "/v2/orders/{order_id}/confirm")

    def test_dynamic_prefix_keeps_suffix_and_limitation(self):
        fs = facts_of({"routes.py": ROUTER, "main.py": "import os\nfrom fastapi import FastAPI\nfrom routes import router\n"
                       "app = FastAPI()\napp.include_router(router, prefix=os.environ['P'])\n"})
        [r] = kind(fs, "route")
        self.assertEqual(val(r, "path"), "unknown")
        self.assertEqual(val(r, "path_suffix"), "/orders/{order_id}/confirm")
        self.assertIn("RUNTIME_DEPENDENT_PREFIX", [x["code"] for x in fs["limitations"]])

    def test_router_never_mounted_is_not_a_route(self):
        fs = facts_of({"routes.py": ROUTER})
        self.assertEqual(kind(fs, "route"), [])
        self.assertIn("ROUTER_NOT_MOUNTED", [x["code"] for x in fs["limitations"]])

    def test_request_and_response_models(self):
        fs = facts_of({"main.py": "from fastapi import FastAPI\nfrom pydantic import BaseModel\n"
                       "class In(BaseModel):\n    name: str\n    note: str | None = None\n"
                       "class Out(In):\n    id: int\n"
                       "app = FastAPI()\n@app.post('/items', response_model=Out, status_code=201)\n"
                       "def create(body: In, q: int = 0):\n    return {}\n"})
        [r] = kind(fs, "route")
        bodies = val(r, "bodies")
        self.assertEqual([b["direction"] for b in bodies], ["request", "response"])
        self.assertEqual(bodies[1]["status"], 201)
        [req] = kind(fs, "request_model")
        fields = {f["name"]["value"]: (f["required"]["value"], f["nullable"]["value"]) for f in val(req, "fields")}
        self.assertEqual(fields, {"name": (True, False), "note": (False, True)})
        [resp] = kind(fs, "response_model")
        self.assertEqual(sorted(f["name"]["value"] for f in val(resp, "fields")), ["id", "name", "note"])
        [q] = val(r, "parameters")
        self.assertEqual((q["name"]["value"], q["in"]["value"], q["required"]["value"]), ("q", "query", False))
        self.assertEqual(r["confidence"], "inferred")  # media type comes from rule fastapi-defaults-v1


class Tables(unittest.TestCase):
    def test_sqlalchemy2_mapped_and_binding(self):
        fs = facts_of({"m.py": "from typing import Optional\nfrom sqlalchemy import ForeignKey, String, create_engine\n"
                       "from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column\n"
                       "class Base(DeclarativeBase):\n    pass\n"
                       "class User(Base):\n    __tablename__ = 'users'\n    id: Mapped[int] = mapped_column(primary_key=True)\n"
                       "    name: Mapped[str] = mapped_column(String(30))\n    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey('team.id'))\n"
                       "engine = create_engine('postgresql://h/db')\nBase.metadata.create_all(engine)\n"})
        [t] = kind(fs, "table")
        cols = {c["name"]["value"]: (c["type"]["value"], c["nullable"]["value"]) for c in val(t, "columns")}
        self.assertEqual(cols, {"id": ("INTEGER", False), "name": ("VARCHAR(30)", False), "team_id": ("INTEGER", True)})
        self.assertEqual(val(t, "dialect"), "postgresql")

    def test_sqlmodel_inherited_fields_and_default_name(self):
        fs = facts_of({"m.py": "from sqlmodel import Field, Relationship, SQLModel\n"
                       "class HeroBase(SQLModel):\n    name: str\n    team_id: int | None = Field(default=None, foreign_key='team.id')\n"
                       "class Hero(HeroBase, table=True):\n    id: int | None = Field(default=None, primary_key=True)\n"
                       "    team: 'Team' = Relationship()\n"})
        [t] = kind(fs, "table")
        self.assertEqual(val(t, "name"), "hero")
        self.assertEqual(sorted(c["name"]["value"] for c in val(t, "columns")), ["id", "name", "team_id"])
        self.assertEqual(t["confidence"], "inferred")

    def test_table_variable(self):
        fs = facts_of({"m.py": "from sqlalchemy import Column, ForeignKey, Integer, Table\nfrom sqlalchemy.orm import declarative_base\n"
                       "Base = declarative_base()\nassoc = Table('assoc', Base.metadata, Column('a_id', Integer, ForeignKey('a.id')))\n"})
        [t] = kind(fs, "table")
        self.assertEqual(val(t, "name"), "assoc")
        self.assertEqual(val(t, "columns")[0]["foreign_key"]["value"], {"table": "a", "column": "id"})


class Events(unittest.TestCase):
    def test_kafka_producer_and_consumer_are_extracted(self):
        fs = facts_of({"orders.py": "import json\nfrom kafka import KafkaProducer\n"
                       "p = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode())\n"
                       "def place():\n    p.send('order-created', {'id': 1})\n",
                       "stock.py": "import json\nfrom kafka import KafkaConsumer\n"
                       "c = KafkaConsumer('order-created', bootstrap_servers='kafka:9092', value_deserializer=json.loads)\n"})
        events = {val(e, "action"): e for e in kind(fs, "event")}
        self.assertEqual(sorted(events), ["consume", "publish"])
        for e in events.values():
            self.assertEqual((val(e, "topic"), val(e, "broker"), val(e, "serialization_context")),
                             ("order-created", "kafka:kafka:9092", "json"))
            self.assertEqual(e["attributes"]["namespace"]["state"], "not_applicable")

    def test_faststream_decorators(self):
        fs = facts_of({"svc.py": "from faststream.kafka import KafkaBroker\nbroker = KafkaBroker('localhost:9092')\n"
                       "@broker.subscriber('in')\n@broker.publisher('out')\nasync def handle(m):\n    return m\n"})
        self.assertEqual(sorted((val(e, "action"), val(e, "topic")) for e in kind(fs, "event")),
                         [("consume", "in"), ("publish", "out")])


class OtherFacts(unittest.TestCase):
    def test_http_config_library(self):
        fs = facts_of({"c.py": "import os, httpx\nURL = os.getenv('PAYMENT_URL')\nTOKEN = os.environ['API_TOKEN']\n"
                       "def pay():\n    httpx.post('https://pay.local/charge?x=1')\n",
                       "requirements.txt": "fastapi>=0.110\nhttpx\n"})
        [h] = kind(fs, "http_call")
        self.assertEqual((val(h, "method"), val(h, "url")), ("POST", "https://pay.local/charge"))
        cfg = {val(c, "key"): c["attributes"]["value"]["state"] for c in kind(fs, "config")}
        self.assertEqual(cfg, {"PAYMENT_URL": "unknown", "API_TOKEN": "redacted"})
        self.assertEqual(sorted(val(l, "name") for l in kind(fs, "library")), ["fastapi", "httpx"])


class References(unittest.TestCase):
    def refs(self, files):
        fs = facts_of(files)
        return {(val(f, "source_symbol"), val(f, "target_symbol"), val(f, "reference_kind")): f for f in kind(fs, "reference")}

    def test_module_level_and_value_flow(self):
        refs = self.refs({"main.py": "class A:\n    def func(self):\n        pass\n"
                          "def give():\n    return A\n"
                          "def call(f):\n    f()\n"
                          "a = A()\na.func()\nB = give()\ncall(give)\n"})
        self.assertIn(("main.__module__", "main.A", "calls"), refs)
        self.assertEqual(refs[("main.__module__", "main.A.func", "calls")]["confidence"], "inferred")
        self.assertIn(("main.call", "main.give", "calls"), refs)

    def test_depends_via_annotated_alias(self):
        refs = self.refs({"deps.py": "from typing import Annotated\nfrom fastapi import Depends\n"
                          "def get_db():\n    return None\nDb = Annotated[object, Depends(get_db)]\n",
                          "main.py": "from fastapi import FastAPI\nfrom deps import Db\napp = FastAPI()\n"
                          "@app.get('/x')\ndef x(db: Db):\n    return 1\n"})
        self.assertIn(("main.x", "deps.get_db", "depends"), refs)

    def test_dynamic_import_is_unresolved_not_dropped(self):
        refs = self.refs({"m.py": "import importlib\ndef run(name):\n    plugin = importlib.import_module(name)\n"
                          "    plugin.notify()\n"})
        [f] = [f for k, f in refs.items() if k[0] == "m.run"]
        self.assertEqual(f["resolution"], "unresolved")
        self.assertEqual(val(f, "call_text"), "plugin.notify")

    def test_unresolved_calls_are_listed_as_a_limitation(self):
        """KPI-010 (OBS-001): a relation whose target is unknown appears in the limitations of the run."""
        fs = facts_of({"m.py": "import importlib\ndef run(name):\n    plugin = importlib.import_module(name)\n"
                       "    plugin.notify()\n"})
        [f] = [f for f in kind(fs, "reference") if f["resolution"] == "unresolved"]
        [lim] = [x for x in fs["limitations"] if x["code"] == "REFERENCE_UNRESOLVED"]
        self.assertEqual(lim["affected_ids"], [f["id"]])


PACKAGE = {  # rhoboro layout: a package __init__.py re-exports names defined in its modules
    "models/__init__.py": "from .notes import Note\nfrom .schema import NoteSchema\n",
    "models/notes.py": "class Note:\n    @classmethod\n    def create(cls, title):\n        return cls()\n",
    "models/schema.py": "from pydantic import BaseModel\nclass NoteSchema(BaseModel):\n    id: int\n    title: str\n",
    "service.py": "from models import Note\ndef create_note(title):\n    return Note.create(title)\n",
    "api.py": "from fastapi import FastAPI\nfrom models import NoteSchema\nfrom service import create_note\n"
              "class CreateNoteResponse(NoteSchema):\n    pass\n"
              "app = FastAPI()\n@app.post('/notes', response_model=CreateNoteResponse)\n"
              "def create(title: str):\n    return create_note(title)\n",
}


FORM = "from pydantic import BaseModel\nclass Form(BaseModel):\n    username: str\n"


class RepoLayouts(unittest.TestCase):
    """Shapes seen on Khiem's open repos (fullstack, realworld, teamhide), 02/10/2026."""

    def test_package_under_a_plain_folder_is_imported_by_its_own_name(self):
        # fullstack: backend/ is not a package; code imports `from app.api import router`
        fs = facts_of({"backend/app/__init__.py": "", "backend/app/api.py": ROUTER,
                       "backend/app/main.py": "from fastapi import FastAPI\nfrom app.api import router\n"
                                              "app = FastAPI()\napp.include_router(router, prefix='/v1')\n"})
        [r] = kind(fs, "route")
        self.assertEqual(val(r, "path"), "/v1/orders/{order_id}/confirm")

    def test_depends_without_argument_and_annotated_alias_are_not_parameters(self):
        # fullstack: `form_data: Annotated[Form, Depends()]`, `current_user: CurrentUser` (alias with Depends)
        fs = facts_of({"forms.py": FORM,
                       "deps.py": "from typing import Annotated\nfrom fastapi import Depends\nfrom forms import Form\n"
                                  "def get_user():\n    return None\nCurrentUser = Annotated[Form, Depends(get_user)]\n",
                       "main.py": "from typing import Annotated\nfrom fastapi import FastAPI, Depends\nfrom forms import Form\n"
                                  "from deps import CurrentUser\napp = FastAPI()\n"
                                  "@app.post('/login')\ndef login(form_data: Annotated[Form, Depends()], user: CurrentUser,"
                                  " other: Form = Depends(), q: int = 0):\n    return {}\n"})
        [r] = kind(fs, "route")
        self.assertEqual([p["name"]["value"] for p in val(r, "parameters")], ["q"])
        self.assertEqual(val(r, "request_model_ids"), [])

    def test_type_from_an_unreadable_file_is_not_called_query(self):
        # fullstack: deps.py uses Python 3.14 syntax, so `session: SessionDep` cannot be classified
        fs = facts_of({"deps.py": "SessionDep = (\n", "main.py": "from fastapi import FastAPI\nfrom deps import SessionDep\n"
                       "app = FastAPI()\n@app.get('/items')\ndef items(session: SessionDep, limit: int = 10):\n    return []\n"})
        [r] = kind(fs, "route")
        session, limit = val(r, "parameters")
        self.assertEqual((session["name"]["value"], session["in"]["state"]), ("session", "unknown"))
        self.assertEqual((limit["name"]["value"], limit["in"]["value"]), ("limit", "query"))

    def test_path_parameter_declared_in_a_dependency(self):
        # realworld: `article = Depends(get_article_by_slug_from_path)` with `slug: str = Path(...)` inside
        fs = facts_of({"main.py": "from fastapi import FastAPI, Depends, Path, Query\napp = FastAPI()\n"
                       "def get_page(offset: int = Query(0)):\n    return offset\n"
                       "def get_article(slug: str = Path(..., min_length=1), page = Depends(get_page)):\n    return slug\n"
                       "@app.get('/articles/{slug}')\ndef read(article = Depends(get_article)):\n    return {}\n"})
        [r] = kind(fs, "route")
        got = {p["name"]["value"]: (p["in"]["value"], p["required"]["value"]) for p in val(r, "parameters")}
        self.assertEqual(got, {"slug": ("path", True), "offset": ("query", False)})

    def test_path_parameter_nowhere_to_be_found_makes_parameters_unknown(self):
        fs = facts_of({"main.py": "from fastapi import FastAPI, Depends\nfrom lib import get_x\napp = FastAPI()\n"
                       "@app.get('/x/{x_id}')\ndef read(x = Depends(get_x)):\n    return {}\n"})
        [r] = kind(fs, "route")
        self.assertEqual(r["attributes"]["parameters"]["state"], "unknown")

    def test_mixin_through_star_reexport_and_composite_columns(self):
        # teamhide: `from .timestamp_mixin import *` in mixins/__init__.py; `composite(mapped_column("lat"), ...)`
        fs = facts_of({
            "db/__init__.py": "from sqlalchemy.orm import DeclarativeBase\nclass Base(DeclarativeBase):\n    pass\n",
            "db/mixins/__init__.py": "from .timestamp_mixin import *\n",
            "db/mixins/timestamp_mixin.py": "from datetime import datetime\nfrom sqlalchemy.orm import Mapped, mapped_column\n"
                                            "class TimestampMixin:\n    created_at: Mapped[datetime] = mapped_column(nullable=False)\n",
            "user.py": "from sqlalchemy.orm import Mapped, mapped_column, composite\nfrom db import Base\n"
                       "from db.mixins import TimestampMixin\nclass User(Base, TimestampMixin):\n    __tablename__ = 'user'\n"
                       "    id: Mapped[int] = mapped_column(primary_key=True)\n"
                       "    location: Mapped[object] = composite(mapped_column('lat'), mapped_column('lng'))\n"})
        [t] = kind(fs, "table")
        self.assertEqual([c["name"]["value"] for c in val(t, "columns")], ["created_at", "id", "lat", "lng"])

    def test_tables_created_only_in_migrations_are_a_limitation(self):
        # realworld: tables come from `op.create_table(...)` in an Alembic migration, raw SQL elsewhere
        fs = facts_of({"migrations/versions/001_main.py": "import sqlalchemy as sa\nfrom alembic import op\n"
                       "def upgrade():\n    op.create_table('users', sa.Column('id', sa.Integer, primary_key=True))\n"
                       "    op.create_table('articles', sa.Column('id', sa.Integer))\n"})
        self.assertEqual(kind(fs, "table"), [])
        [lim] = [x for x in fs["limitations"] if x["code"] == "TABLES_IN_MIGRATIONS_NOT_READ"]
        self.assertIn("users", lim["message"])
        self.assertIn("articles", lim["message"])

    def test_migration_of_a_table_already_read_from_its_model_is_not_reported(self):
        # fullstack, teamhide: the model and the migration both declare the table
        fs = facts_of({"m.py": "from sqlalchemy import Column, Integer\nfrom sqlalchemy.orm import declarative_base\n"
                       "Base = declarative_base()\nclass User(Base):\n    __tablename__ = 'users'\n"
                       "    id = Column(Integer, primary_key=True)\n",
                       "migrations/versions/001.py": "import sqlalchemy as sa\nfrom alembic import op\n"
                       "def upgrade():\n    op.create_table('users', sa.Column('id', sa.Integer))\n"})
        self.assertEqual(len(kind(fs, "table")), 1)
        self.assertNotIn("TABLES_IN_MIGRATIONS_NOT_READ", [x["code"] for x in fs["limitations"]])


class LibrariesAndQueues(unittest.TestCase):
    """Đề bài 3.6: important dependency, queue/event (02/10/2026)."""

    def test_library_used_from_imports(self):
        fs = facts_of({"requirements.txt": "fastapi>=0.110\npydantic-settings\npsycopg2-binary\nasyncpg\npython-slugify\n",
                       "main.py": "import fastapi\nfrom pydantic_settings import BaseSettings\nimport psycopg2\n"
                                  "from slugify import slugify\n"})
        got = {val(f, "name"): f["attributes"]["used"] for f in kind(fs, "library")}
        self.assertEqual({k: v["state"] for k, v in got.items()},
                         {"fastapi": "known", "pydantic-settings": "known", "psycopg2-binary": "known", "asyncpg": "unknown",
                          "python-slugify": "known"})
        self.assertTrue(all(v["value"] is True for v in got.values() if v["state"] == "known"))
        self.assertIn("Không thấy import", got["asyncpg"]["reason"])

    def test_unsupported_queue_library_is_a_limitation(self):
        # Celery is read since 11/10/2026 (FR-031); dramatiq still has no event rule
        fs = facts_of({"jobs/__init__.py": "import dramatiq\nbroker = dramatiq.get_broker()\n"})
        [lim] = [x for x in fs["limitations"] if x["code"] == "QUEUE_LIBRARY_UNSUPPORTED"]
        self.assertIn("dramatiq", lim["message"])
        self.assertIn("jobs/__init__.py", lim["message"])


class NestedModels(unittest.TestCase):
    def test_model_inside_a_field_and_none_response(self):
        # rhoboro: `notebooks: list[NotebookSchema]`; `def delete(...) -> None` with status 204
        fs = facts_of({"main.py": "from fastapi import FastAPI\nfrom pydantic import BaseModel\n"
                       "class Note(BaseModel):\n    id: int\nclass Book(BaseModel):\n    notes: list[Note]\n"
                       "app = FastAPI()\n@app.get('/books', response_model=Book)\ndef books():\n    return None\n"
                       "@app.delete('/books/{book_id}', status_code=204)\ndef drop(book_id: int) -> None:\n    pass\n"})
        models = {val(m, "name"): m for m in kind(fs, "response_model")}
        notes = val(models["main.Book"], "fields")[0]["type"]["value"]
        self.assertEqual(notes, {"type": "array", "items": {"x-model-fact": models["main.Note"]["id"]}})
        drop = next(r for r in kind(fs, "route") if val(r, "method") == "DELETE")
        self.assertEqual(val(drop, "response_model_ids"), [])

    def test_string_formats(self):
        # fullstack: `id: uuid.UUID`, `created_at: datetime | None`, `email: EmailStr`
        fs = facts_of({"main.py": "import uuid\nfrom datetime import datetime\nfrom fastapi import FastAPI\n"
                       "from pydantic import BaseModel, EmailStr\nclass U(BaseModel):\n    id: uuid.UUID\n"
                       "    created_at: datetime | None = None\n    email: EmailStr\n"
                       "app = FastAPI()\n@app.get('/u', response_model=U)\ndef u():\n    return None\n"})
        [m] = kind(fs, "response_model")
        got = {f["name"]["value"]: f["type"]["value"] for f in val(m, "fields")}
        self.assertEqual(got, {"id": {"type": "string", "format": "uuid"},
                               "created_at": {"type": "string", "format": "date-time"},
                               "email": {"type": "string", "format": "email"}})


class NamedRules(unittest.TestCase):
    """Values taken from a documented default carry the rule name and `inferred` (API-004, revision 02/10/2026)."""

    def test_status_default_and_status_constant(self):
        fs = facts_of({"main.py": "from fastapi import FastAPI, status\napp = FastAPI()\n"
                       "@app.get('/a')\ndef a():\n    return 1\n"
                       "@app.post('/b', status_code=status.HTTP_201_CREATED)\ndef b():\n    return 1\n"})
        got = {val(r, "path"): (val(r, "status_codes"), val(r, "status_rule"), r["confidence"]) for r in kind(fs, "route")}
        self.assertEqual(got["/a"], ([200], "fastapi-status-default-v1", "inferred"))
        self.assertEqual(got["/b"], ([201], "starlette-status-constant-v1", "inferred"))

    def test_prefix_from_settings_default(self):
        # fullstack: app.include_router(api_router, prefix=settings.API_V1_STR); API_V1_STR: str = "/api/v1"
        fs = facts_of({"config.py": "from pydantic_settings import BaseSettings\nclass Settings(BaseSettings):\n"
                                    "    API_V1_STR: str = '/api/v1'\nsettings = Settings()\n",
                       "routes.py": ROUTER,
                       "main.py": "from fastapi import FastAPI\nfrom routes import router\nfrom config import settings\n"
                                  "app = FastAPI()\napp.include_router(router, prefix=settings.API_V1_STR)\n"})
        [r] = kind(fs, "route")
        self.assertEqual(val(r, "path"), "/api/v1/orders/{order_id}/confirm")
        self.assertEqual(val(r, "prefix_rule"), "settings-default-v1")
        self.assertEqual(r["confidence"], "inferred")

    def test_prefix_from_a_settings_factory_inside_the_app_factory(self):
        # realworld: def get_application(): settings = get_app_settings(); ...prefix=settings.api_prefix
        cfg = ("from pydantic_settings import BaseSettings\nclass AppSettings(BaseSettings):\n    api_prefix: str = '/api'\n"
               "class Dev(AppSettings):\n    debug: bool = True\n{extra}"
               "def get_app_settings() -> AppSettings:\n    return Dev()\n")
        main = ("from fastapi import FastAPI\nfrom routes import router\nfrom config import get_app_settings\n"
                "def get_application():\n    settings = get_app_settings()\n    app = FastAPI()\n"
                "    app.include_router(router, prefix=settings.api_prefix)\n    return app\n")
        fs = facts_of({"config.py": cfg.format(extra=""), "routes.py": ROUTER, "main.py": main})
        [r] = kind(fs, "route")
        self.assertEqual(val(r, "path"), "/api/orders/{order_id}/confirm")
        # a subclass with another default: the value depends on which class runs, so the path stays unknown
        fs = facts_of({"config.py": cfg.format(extra="class Prod(AppSettings):\n    api_prefix: str = '/v2'\n"),
                       "routes.py": ROUTER, "main.py": main})
        [r] = kind(fs, "route")
        self.assertEqual(r["attributes"]["path"]["state"], "unknown")

    def test_auth_reason_names_the_dependencies(self):
        fs = facts_of({"main.py": "from fastapi import FastAPI, Depends\napp = FastAPI()\ndef admin():\n    return 1\n"
                       "@app.get('/x', dependencies=[Depends(admin)])\ndef x():\n    return 1\n"})
        [r] = kind(fs, "route")
        self.assertIn("admin", r["attributes"]["auth"]["reason"])

    def test_column_type_reason_keeps_the_declared_type(self):
        fs = facts_of({"m.py": "from sqlalchemy import Column, String\nfrom sqlalchemy.orm import declarative_base\n"
                       "Base = declarative_base()\nclass U(Base):\n    __tablename__ = 'u'\n"
                       "    name = Column(String(64), primary_key=True)\n"})
        [t] = kind(fs, "table")
        self.assertIn("String(64)", val(t, "columns")[0]["type"]["reason"])


class ReExports(unittest.TestCase):
    def test_call_through_package_reexport_is_resolved(self):
        fs = facts_of(PACKAGE)
        refs = {(val(f, "source_symbol"), val(f, "target_symbol")): f for f in kind(fs, "reference")}
        self.assertEqual(refs[("service.create_note", "models.notes.Note.create")]["resolution"], "resolved")

    def test_response_model_inheriting_a_reexported_model(self):
        fs = facts_of(PACKAGE)
        [r] = kind(fs, "route")
        [resp] = [f for f in kind(fs, "response_model") if f["id"] in val(r, "response_model_ids")]
        self.assertEqual(val(resp, "name"), "api.CreateNoteResponse")
        self.assertEqual(sorted(x["name"]["value"] for x in val(resp, "fields")), ["id", "title"])


if __name__ == "__main__":
    unittest.main()
