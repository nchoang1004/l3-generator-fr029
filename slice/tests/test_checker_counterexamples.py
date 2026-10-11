"""Counterexamples to the FR-029 checker from the independent Codex review of 08/10/2026 (fairness audit).

Each test is one piece of FastAPI code the review showed the checker gets wrong: a false acceptance, a false
rejection, a wrong or missing parameter reminder, or an HTTP call the suspect scan would not flag.
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE)]

from l3slice.docfacts import Claims  # noqa: E402
from test_docagent import tools_for  # noqa: E402


def claims_of(files: dict) -> Claims:
    tools = tools_for(files)
    for p in files:
        for i in range(1, len(tools.lines[p]) + 1):
            tools.state[p][i] = "processed"
    return Claims(tools)


def route(handler, decorator, path, method="GET", deps=(), application="main.py:3"):
    return {"method": method, "handler": handler, "decorator": decorator, "application": application,
            "path_parts": [{"kind": "decorator", "value": path, "at": decorator.split("-")[0]}], "params": [],
            "request_body": None, "response": None, "dependencies": [{"name": n, "at": at} for n, at in deps],
            "status": {"codes": [200], "rule": "fastapi.default_status_200"}, "auth": {"unknown": "chưa rõ"}}


def reminders(claims) -> str:
    return " ".join(p for p in claims.open_problems([]) if "dependency" in p)


MAIN = "from fastapi import FastAPI, Depends\n{imports}\napp = FastAPI()\n\n\n{decorator}\n{signature}\n    pass\n"


def main_py(imports, decorator, signature):
    return MAIN.format(imports=imports, decorator=decorator, signature=signature)


class Dependencies(unittest.TestCase):
    def test_alias_is_resolved_through_the_import(self):
        dep = ("from typing import Annotated\nfrom fastapi import Depends, Header\n\n\n"
               "def dep_{x}(x_{x}: str = Header()):\n    return x_{x}\n\n\nUserDep = Annotated[str, Depends(dep_{x})]\n")
        c = claims_of({"a.py": dep.format(x="a"), "b.py": dep.format(x="b"),
                       "main.py": main_py("from a import UserDep", '@app.get("/e")', "def e(u: UserDep):")})
        self.assertTrue(c.dependency_at("dep_a", ("main.py", 7, 7)))
        self.assertFalse(c.dependency_at("dep_b", ("main.py", 7, 7)))
        self.assertEqual(c.submit({"routes": [route("main.py::e", "main.py:6-7", "/e", deps=[("dep_a", "main.py:7")])]})
                         ["errors"], [])
        self.assertIn("'x-a'", reminders(c))
        self.assertNotIn("'x-b'", reminders(c))

    def test_class_method_keeps_its_class(self):
        classes = ("from fastapi import Depends, Header\n\n\nclass A:\n    @staticmethod\n    def inject(x_a: str = Header()):\n"
                   "        return x_a\n\n\nclass B:\n    @staticmethod\n    def inject(x_b: str = Header()):\n        return x_b\n\n\n"
                   "def outer(v=Depends(B.inject)):\n    return v\n")
        c = claims_of({"deps.py": classes,
                       "main.py": main_py("from deps import B, outer", '@app.get("/e")',
                                          "def e(b=Depends(B.inject), o=Depends(outer)):")})
        self.assertFalse(c.dependency_at("A.inject", ("main.py", 7, 7)))
        self.assertTrue(c.dependency_at("B.inject", ("main.py", 7, 7)))
        c.submit({"routes": [route("main.py::e", "main.py:6-7", "/e", deps=[("outer", "main.py:7")])]})
        self.assertIn("'x-b'", reminders(c))

    def test_factory_only_when_called(self):
        deps = ("from fastapi import Query\n\n\ndef provider(q: str):\n    def inner(x: str = Query(...)):\n        return x\n"
                "    return inner\n")
        plain = claims_of({"deps.py": deps, "main.py": main_py("from deps import provider", '@app.get("/e")',
                                                              "def e(value=Depends(provider)):")})
        plain.submit({"routes": [route("main.py::e", "main.py:6-7", "/e", deps=[("provider", "main.py:7")])]})
        self.assertIn("'q'", reminders(plain))
        self.assertNotIn("'x'", reminders(plain))
        called = claims_of({"deps.py": deps, "main.py": main_py("from deps import provider", '@app.get("/e")',
                                                               "def e(value=Depends(provider(\"cfg\"))):")})
        called.submit({"routes": [route("main.py::e", "main.py:6-7", "/e", deps=[("provider", "main.py:7")])]})
        self.assertIn("'x'", reminders(called))
        self.assertNotIn("'q'", reminders(called))

    def test_scalar_named_in_the_path_is_a_path_parameter(self):
        c = claims_of({"deps.py": "def identify(item_id: int):\n    return item_id\n",
                       "main.py": main_py("from deps import identify", '@app.get("/items/{item_id}")',
                                          "def e(value=Depends(identify)):")})
        c.submit({"routes": [route("main.py::e", "main.py:6-7", "/items/{item_id}", deps=[("identify", "main.py:7")])]})
        self.assertIn("path 'item_id'", reminders(c))
        self.assertNotIn("query 'item_id'", reminders(c))

    def test_string_annotation_is_a_scalar(self):
        c = claims_of({"deps.py": "def search(q: 'str'):\n    return q\n",
                       "main.py": main_py("from deps import search", '@app.get("/e")', "def e(value=Depends(search)):")})
        c.submit({"routes": [route("main.py::e", "main.py:6-7", "/e", deps=[("search", "main.py:7")])]})
        self.assertIn("query 'q'", reminders(c))


class Routes(unittest.TestCase):
    def test_factory_must_return_the_app(self):
        fake = ("from fastapi import FastAPI\n\n\nclass Registry:\n    def get(self, path):\n        return lambda fn: fn\n\n\n"
                "def build():\n    unused = FastAPI()\n    return Registry()\n\n\nrouter = build()\n\n\n"
                "@router.get('/fake')\ndef fake():\n    return {}\n")
        self.assertTrue(claims_of({"m.py": fake})._decorator_problems(("m.py", 17, 18), "m.py::fake", "GET"))

    def test_factory_chain_returning_the_app(self):
        real = ("from fastapi import FastAPI\n\n\ndef build():\n    return FastAPI()\n\n\ndef create():\n    return build()\n\n\n"
                "app = create()\n\n\n@app.get('/real')\ndef real():\n    return {}\n")
        self.assertEqual(claims_of({"m.py": real})._decorator_problems(("m.py", 15, 16), "m.py::real", "GET"), [])

    def test_imported_receiver_that_is_not_fastapi(self):
        files = {"hooks.py": "class Registry:\n    def get(self, path):\n        return lambda fn: fn\n\n\nregistry = Registry()\n",
                 "orders.py": "from hooks import registry\n\n\n@registry.get('/orders/cached')\ndef cached_orders():\n"
                              "    return []\n"}
        self.assertTrue(claims_of(files)._decorator_problems(("orders.py", 4, 5), "orders.py::cached_orders", "GET"))

    def test_imported_router_is_still_accepted(self):
        files = {"routers.py": "from fastapi import APIRouter\nrouter = APIRouter()\n",
                 "views.py": "from routers import router\n\n\n@router.get('/x')\ndef x():\n    return []\n"}
        self.assertEqual(claims_of(files)._decorator_problems(("views.py", 4, 5), "views.py::x", "GET"), [])

    def test_api_route_method_must_be_in_methods(self):
        c = claims_of({"m.py": "from fastapi import FastAPI\napp = FastAPI()\n\n\n"
                               "@app.api_route('/x', methods=['GET'], name='POST')\ndef endpoint():\n    return {}\n"})
        self.assertEqual(c._decorator_problems(("m.py", 5, 6), "m.py::endpoint", "GET"), [])
        self.assertTrue(c._decorator_problems(("m.py", 5, 6), "m.py::endpoint", "POST"))


def http(c, at, library, method, value):
    target = {"kind": "literal", "value": value} if value else {"kind": "unknown", "reason": "?"}
    return c.add_http({"at": at, "library": library, "method": method, "target": target})


class HttpClaims(unittest.TestCase):
    def test_library_must_match_the_module_called(self):
        c = claims_of({"h.py": "import httpx\nimport requests\nrequests.get('https://api.example/items')\n"})
        self.assertTrue(http(c, "h.py:3", "httpx", "GET", "https://api.example/items"))
        self.assertEqual(http(c, "h.py:3", "requests", "GET", "https://api.example/items"), [])

    def test_receiver_must_be_an_http_client(self):
        c = claims_of({"h.py": "import httpx\nfrom bs4 import BeautifulSoup\n\n\ndef links(html):\n"
                               "    for link in BeautifulSoup(html).find_all('a'):\n        yield link.get('href')\n\n\n"
                               "def fetch():\n    with httpx.Client() as c:\n        return c.get('https://a.example')\n"})
        self.assertTrue(http(c, "h.py:7", "httpx", "GET", None))
        self.assertEqual(http(c, "h.py:12", "httpx", "GET", "https://a.example"), [])

    def test_library_of_a_client_variable(self):
        c = claims_of({"h.py": "import httpx\nimport requests\n\n\ndef f():\n    c = httpx.Client()\n"
                               "    return c.get('https://a.example')\n"})
        self.assertTrue(http(c, "h.py:7", "requests", "GET", "https://a.example"))
        self.assertEqual(http(c, "h.py:7", "httpx", "GET", "https://a.example"), [])

    def test_a_name_like_session_is_not_enough_for_a_claim(self):
        c = claims_of({"h.py": "import aiohttp\n\n\nclass Installer:\n    async def drop(self, creds):\n"
                               "        await self.crud.session.delete(creds)\n"})
        self.assertTrue(http(c, "h.py:6", "aiohttp", "DELETE", None))
        self.assertIn("h.py:6", [s["at"] for s in c.suspects()])  # still a suspect the agent must look at

    def test_local_client_name_does_not_cover_an_attribute(self):
        c = claims_of({"h.py": "import aiohttp\n\n\nclass Installer:\n    async def token(self):\n"
                               "        async with aiohttp.ClientSession() as session:\n"
                               "            await session.post('https://a.example')\n\n"
                               "    async def drop(self, creds):\n        await self.crud.session.delete(creds)\n"})
        self.assertEqual(http(c, "h.py:7", "aiohttp", "POST", "https://a.example"), [])
        self.assertTrue(http(c, "h.py:10", "aiohttp", "DELETE", None))

    def test_url_is_read_inside_the_call_only(self):
        c = claims_of({"h.py": "import httpx\nhttpx.get('https://real.example'); note = dict(url='https://decoy.example')\n"})
        self.assertTrue(http(c, "h.py:2", "httpx", "GET", "https://decoy.example"))
        self.assertEqual(http(c, "h.py:2", "httpx", "GET", "https://real.example"), [])

    def test_a_literal_prefix_is_not_the_url(self):
        c = claims_of({"h.py": "import httpx\nsuffix = 'x'\nhttpx.get('https://real.example' + suffix)\n"})
        self.assertTrue(http(c, "h.py:3", "httpx", "GET", "https://real.example"))

    def test_comment_parenthesis_and_multiline_request_method(self):
        c = claims_of({"h.py": "import httpx\nhttpx.get(  # )\n    'https://api.example/items'\n)\n"
                               "httpx.request(\n    'GET',\n    'https://api.example/other'\n)\n"})
        self.assertEqual(http(c, "h.py:2", "httpx", "GET", "https://api.example/items"), [])
        self.assertEqual(http(c, "h.py:5", "httpx", "GET", "https://api.example/other"), [])

    def test_request_with_a_method_variable(self):
        c = claims_of({"h.py": "import httpx\nverb = 'GET'\nhttpx.request(verb, 'https://api.example/items')\n"})
        self.assertEqual(c.add_http({"at": "h.py:3", "library": "httpx", "method": {"unknown": "biến"},
                                     "target": {"kind": "literal", "value": "https://api.example/items"}}), [])


class SuspectRecall(unittest.TestCase):
    """Every real httpx/requests/aiohttp call must be flagged, or the agent can skip it unnoticed."""
    CASES = {
        "comma_import": "import os, httpx\nhttpx.get('https://a.example')\n",
        "bare_import": "from requests import get\nget('https://a.example')\n",
        "aliased_import": "from httpx import get as fetch\nfetch('https://a.example')\n",
        "constructor_alias": "from httpx import Client as C\nc = C()\nc.get('https://a.example')\n",
        "rebound": "import httpx\nc = httpx.Client()\nwire = c\nwire.get('https://a.example')\n",
        "subclass": "import httpx\n\n\nclass Transport(httpx.Client):\n    pass\n\n\nwire = Transport()\nwire.get('https://a.example')\n",
        "lowercase_session": "import requests\nwire = requests.session()\nwire.get('https://a.example')\n",
        "send": "import httpx\nc = httpx.Client()\nc.send(httpx.Request('GET', 'https://a.example'))\n",
        "after_string": "import requests\ntext = '''a\nb'''; requests.get('https://a.example')\n",
        "contextmanager": ("import aiohttp\nfrom contextlib import asynccontextmanager\n\n\n@asynccontextmanager\n"
                           "async def connection():\n    async with aiohttp.ClientSession() as c:\n        yield c\n\n\n"
                           "async def use():\n    async with connection() as wire:\n        await wire.get('https://a.example')\n"),
    }

    def test_each_form_is_flagged(self):
        for name, src in self.CASES.items():
            with self.subTest(name):
                c = claims_of({"h.py": src})
                last = len(src.rstrip("\n").split("\n"))
                self.assertIn(f"h.py:{last}", [s["at"] for s in c.suspects()])

    def test_client_imported_from_another_module(self):
        c = claims_of({"clients.py": "import httpx\nclient = httpx.Client()\n",
                       "routes.py": "from clients import client\n\n\ndef fetch():\n    return client.get('https://a.example')\n"})
        self.assertIn("routes.py:5", [s["at"] for s in c.suspects()])

    def test_database_session_is_not_an_http_client(self):
        c = claims_of({"repo.py": "from sqlalchemy.orm import Session\n\n\ndef load(engine, item_id):\n"
                                  "    with Session(engine) as session:\n        return session.get(Item, item_id)\n",
                       "cache.py": "import httpx\nfrom redis import Redis\nstore = Redis()\nvalue = store.get('k')\n"})
        self.assertEqual([s["at"] for s in c.suspects()], [])

    def test_dict_named_like_a_client_is_not_flagged(self):
        c = claims_of({"h.py": "import httpx\nclient_cache = {'k': 1}\nvalue = client_cache.get('k')\n"})
        self.assertEqual([s["at"] for s in c.suspects()], [])


class RoundTwo(unittest.TestCase):
    """Second Codex review (08/10/2026): new counterexamples, each reproduced by running the checker."""

    def test_route_path_is_the_decorator_path_argument(self):
        c = claims_of({"main.py": "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/real', name='/fake')\n"
                                  "def e():\n    return {}\n"})
        r = route("main.py::e", "main.py:3-4", "/fake", application="main.py:2")
        self.assertTrue(c.add_route(r))
        self.assertEqual(c.add_route(dict(r, path_parts=[{"kind": "decorator", "value": "/real", "at": "main.py:3"}])), [])

    def test_dependency_name_inside_a_string_is_not_a_dependency(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends, Query\n\n\ndef real():\n    return 1\n\n\n"
                                  "def other(x: str = Query()):\n    return x\n\n\napp = FastAPI()\n\n\n@app.get('/e')\n"
                                  "def e(v=Depends(real), note: str = 'other'):\n    return v\n"})
        self.assertFalse(c.dependency_at("other", ("main.py", 16, 16)))
        self.assertTrue(c.dependency_at("real", ("main.py", 16, 16)))

    def test_same_function_name_in_two_modules(self):
        c = claims_of({"a.py": "from fastapi import Header\n\n\ndef dep(x_a: str = Header()):\n    return x_a\n",
                       "b.py": "from fastapi import Header\n\n\ndef dep(x_b: str = Header()):\n    return x_b\n",
                       "main.py": main_py("from a import dep", '@app.get("/e")', "def e(v=Depends(dep)):")})
        c.submit({"routes": [route("main.py::e", "main.py:6-7", "/e", deps=[("dep", "main.py:7")])]})
        self.assertIn("'x-a'", reminders(c))
        self.assertNotIn("'x-b'", reminders(c))

    def test_convert_underscores_false_keeps_the_name(self):
        c = claims_of({"deps.py": "from fastapi import Header\n\n\n"
                                  "def dep(x_custom: str = Header(convert_underscores=False)):\n    return x_custom\n",
                       "main.py": main_py("from deps import dep", '@app.get("/e")', "def e(v=Depends(dep)):")})
        c.submit({"routes": [route("main.py::e", "main.py:6-7", "/e", deps=[("dep", "main.py:7")])]})
        self.assertIn("'x_custom'", reminders(c))

    def test_unannotated_parameter_is_a_query(self):
        c = claims_of({"deps.py": "def dep(q='abc'):\n    return q\n",
                       "main.py": main_py("from deps import dep", '@app.get("/e")', "def e(v=Depends(dep)):")})
        c.submit({"routes": [route("main.py::e", "main.py:6-7", "/e", deps=[("dep", "main.py:7")])]})
        self.assertIn("query 'q'", reminders(c))

    SCOPES = ("import httpx\n\n\ndef remote():\n    c = httpx.Client()\n    return c.get('https://real.example')\n\n\n"
              "def e():\n    c = {'https://fake.example': 1}\n    return c.get('https://fake.example')\n")

    def test_a_name_is_read_in_its_own_function(self):
        c = claims_of({"h.py": self.SCOPES})
        self.assertTrue(http(c, "h.py:11", "httpx", "GET", "https://fake.example"))
        self.assertEqual(http(c, "h.py:6", "httpx", "GET", "https://real.example"), [])
        self.assertNotIn("h.py:11", [s["at"] for s in c.suspects()])

    def test_unknown_constructor_is_not_ruled_out_and_imported_subclass_is_a_client(self):
        c = claims_of({"inv.py": "import httpx\n\n\nclass InventoryClient(httpx.AsyncClient):\n    pass\n",
                       "h.py": "import httpx\nfrom inv import InventoryClient\n\n\nasync def reserve():\n"
                               "    async with InventoryClient() as client:\n        return await client.put('https://i.example')\n"})
        self.assertIn("h.py:7", [s["at"] for s in c.suspects()])
        self.assertEqual(http(c, "h.py:7", "httpx", "PUT", "https://i.example"), [])

    def test_client_at_is_checked(self):
        c = claims_of({"h.py": "import httpx\n\n\ndef e():\n    cache = {'https://fake.example': 1}\n"
                               "    return cache.get('https://fake.example')\n"})
        self.assertTrue(c.add_http({"at": "h.py:6", "library": "httpx", "method": "GET", "client_at": "nope.py:999",
                                    "target": {"kind": "literal", "value": "https://fake.example"}}))

    def test_client_given_by_depends(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends\nimport httpx\napp = FastAPI()\n\n\n"
                                  "def get_wire():\n    with httpx.Client() as c:\n        yield c\n\n\n@app.get('/e')\n"
                                  "def e(wire=Depends(get_wire)):\n    return wire.get('https://real.example')\n"})
        self.assertIn("main.py:13", [s["at"] for s in c.suspects()])
        self.assertEqual(http(c, "main.py:13", "httpx", "GET", "https://real.example"), [])

    def test_imported_client_with_annotation(self):
        c = claims_of({"clients.py": "import httpx\nwire: httpx.Client = httpx.Client()\n",
                       "main.py": "from clients import wire\n\n\ndef e():\n    return wire.get('https://real.example')\n"})
        self.assertIn("main.py:5", [s["at"] for s in c.suspects()])

    def test_two_calls_on_one_line(self):
        c = claims_of({"h.py": "import httpx\n\n\ndef e():\n"
                               "    httpx.get('https://a.example'); httpx.post('https://b.example')\n"})
        self.assertEqual(http(c, "h.py:5", "httpx", "POST", "https://b.example"), [])
        self.assertIn("h.py:5", [s["at"] for s in c.suspects()])  # the GET is still unaccounted for
        self.assertEqual(http(c, "h.py:5", "httpx", "GET", "https://a.example"), [])
        self.assertEqual(len(c.http), 2)
        self.assertNotIn("h.py:5", [s["at"] for s in c.suspects()])


class RoundThree(unittest.TestCase):
    """Third Codex review (08/10/2026): new counterexamples, each reproduced by running the checker and FastAPI."""

    def test_method_and_path_come_from_the_same_decorator(self):
        c = claims_of({"main.py": "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/read')\n@app.post('/write')\n"
                                  "def e():\n    return {}\n"})
        bad = route("main.py::e", "main.py:3-5", "/write", application="main.py:2")
        bad["path_parts"][0]["at"] = "main.py:4"
        self.assertTrue(c.add_route(bad))
        good = dict(bad, method="POST")
        self.assertEqual(c.add_route(good), [])

    def test_sqlalchemy_session_annotation_is_not_a_client(self):
        c = claims_of({"h.py": "import httpx\nfrom sqlalchemy.orm import Session\n\n\ndef load(db: Session, model, pk):\n"
                               "    return db.get(model, pk)\n"})
        self.assertNotIn("h.py:6", [s["at"] for s in c.suspects()])
        self.assertTrue(http(c, "h.py:6", "httpx", "GET", None))

    def test_provider_imported_from_another_module(self):
        c = claims_of({"clients.py": "import httpx\n\n\ndef get_wire():\n    with httpx.Client() as c:\n        yield c\n",
                       "main.py": "from fastapi import FastAPI, Depends\nfrom clients import get_wire\napp = FastAPI()\n\n\n"
                                  "@app.get('/e')\ndef e(wire=Depends(get_wire)):\n    return wire.get('https://real.example')\n"})
        self.assertIn("main.py:8", [s["at"] for s in c.suspects()])
        self.assertEqual(http(c, "main.py:8", "httpx", "GET", "https://real.example"), [])

    def test_class_dependency_uses_its_init(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends\n\n\nclass Filters:\n"
                                  "    def __init__(self, q: str = ''):\n        self.q = q\n\n\napp = FastAPI()\n\n\n"
                                  "@app.get('/e')\ndef e(filters=Depends(Filters)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:12-13", "/e", application="main.py:9",
                                   deps=[("Filters", "main.py:13")])]})
        self.assertIn("query 'q'", reminders(c))
        self.assertNotIn("'self'", reminders(c))

    def test_renamed_import_of_a_dependency(self):
        c = claims_of({"deps.py": "from fastapi import Header\n\n\ndef dep(x_tenant: str = Header()):\n    return x_tenant\n",
                       "main.py": main_py("from deps import dep as tenant", '@app.get("/e")', "def e(v=Depends(tenant)):")})
        c.submit({"routes": [route("main.py::e", "main.py:6-7", "/e", deps=[("tenant", "main.py:7")])]})
        self.assertIn("'x-tenant'", reminders(c))

    def test_annotated_alias_with_a_marker(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends, Header\nfrom typing import Annotated\n"
                                  "Tenant = Annotated[str, Header(alias='X-Tenant')]\n\n\ndef dep(tenant: Tenant):\n"
                                  "    return tenant\n\n\napp = FastAPI()\n\n\n@app.get('/e')\ndef e(v=Depends(dep)):\n"
                                  "    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:13-14", "/e", application="main.py:10",
                                   deps=[("dep", "main.py:14")])]})
        self.assertIn("header 'X-Tenant'", reminders(c))

    def test_get_on_the_json_result_is_not_a_call(self):
        c = claims_of({"h.py": "import httpx\n\n\ndef fetch_id():\n"
                               "    return httpx.get('https://api.example/item').json().get('id')\n"})
        self.assertEqual(c._http_scan("h.py").http_lines(c._tree("h.py"))[5], 1)
        self.assertEqual(http(c, "h.py:5", "httpx", "GET", "https://api.example/item"), [])
        self.assertTrue(http(c, "h.py:5", "httpx", "GET", "id"))

    def test_library_of_a_client_from_a_helper(self):
        c = claims_of({"h.py": "import httpx\n\n\nclass Evo:\n    def _get_client(self):\n        return httpx.AsyncClient()\n\n"
                               "    async def find(self):\n        async with self._get_client() as client:\n"
                               "            return await client.get('/x')\n"})
        self.assertEqual(http(c, "h.py:10", "httpx", "GET", None), [])
        self.assertTrue(http(c, "h.py:10", "aiohttp", "GET", None))
        self.assertTrue(http(c, "h.py:10", "requests", "GET", None))

    def test_client_at_must_relate_to_the_receiver(self):
        c = claims_of({"h.py": "import httpx\nclient = httpx.Client()\n\n\ndef e():\n"
                               "    cache = {'https://fake.example': 1}\n    return cache.get('https://fake.example')\n"})
        self.assertTrue(c.add_http({"at": "h.py:7", "library": "httpx", "method": "GET", "client_at": "h.py:2",
                                    "target": {"kind": "literal", "value": "https://fake.example"}}))

    def test_two_gets_on_one_line(self):
        c = claims_of({"h.py": "import httpx\n\n\ndef e():\n    httpx.get('https://a.example'); httpx.get('https://b.example')\n"})
        self.assertEqual(http(c, "h.py:5", "httpx", "GET", "https://a.example"), [])
        self.assertEqual(http(c, "h.py:5", "httpx", "GET", "https://b.example"), [])
        self.assertEqual(len(c.http), 2)
        self.assertNotIn("h.py:5", [s["at"] for s in c.suspects()])


class RoundFour(unittest.TestCase):
    """Fourth Codex review (08/10/2026): counterexamples reproduced by running the checker and FastAPI."""

    def test_route_must_be_registered_on_the_claimed_app_with_its_prefixes(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nadmin = FastAPI()\n"
                                  "r = APIRouter()\n\n\n@r.get('/x')\ndef e():\n    return {}\n\n\n"
                                  "app.include_router(r, prefix='/api')\n"})
        base = route("main.py::e", "main.py:7-8", "/x", application="main.py:2")
        self.assertTrue(c.add_route(base))  # the /api prefix of the registration is missing
        self.assertTrue(c.add_route(dict(base, application="main.py:3")))  # admin never includes r
        good = dict(base, path_parts=[{"kind": "include_prefix", "value": "/api", "at": "main.py:12"},
                                      {"kind": "decorator", "value": "/x", "at": "main.py:7"}])
        self.assertEqual(c.add_route(good), [])

    def test_config_key_must_be_the_url_argument(self):
        c = claims_of({"h.py": "import httpx\nfrom types import SimpleNamespace\n"
                               "settings = SimpleNamespace(API_KEY='k', URL='https://real.example')\n\n\n"
                               "def e():\n    return httpx.get(settings.URL, headers={'X-Key': settings.API_KEY})\n"})
        claim = {"at": "h.py:7", "library": "httpx", "method": "GET", "target": {"kind": "config", "value": "API_KEY"}}
        self.assertTrue(c.add_http(claim))
        self.assertEqual(c.add_http(dict(claim, target={"kind": "config", "value": "URL"})), [])

    def test_annotation_keeps_the_library(self):
        c = claims_of({"h.py": "import httpx\nimport requests\n\n\ndef e(wire: httpx.Client):\n"
                               "    return wire.get('https://real.example')\n"})
        self.assertTrue(http(c, "h.py:6", "requests", "GET", "https://real.example"))
        self.assertEqual(http(c, "h.py:6", "httpx", "GET", "https://real.example"), [])

    def test_callable_instance_dependency(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends, Header\n\n\nclass Tenant:\n"
                                  "    def __call__(self, x_tenant: str = Header()):\n        return x_tenant\n\n\n"
                                  "tenant = Tenant()\napp = FastAPI()\n\n\n@app.get('/x')\ndef e(v=Depends(tenant)):\n"
                                  "    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:13-14", "/x", application="main.py:10",
                                   deps=[("tenant", "main.py:14")])]})
        self.assertIn("'x-tenant'", reminders(c))

    def test_literal_and_enum_are_query_parameters(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends\nfrom typing import Literal\nfrom enum import Enum\n\n\n"
                                  "class Order(str, Enum):\n    asc = 'asc'\n    desc = 'desc'\n\n\n"
                                  "def filters(sort: Literal['name', 'date'] = 'name', order: Order = Order.asc):\n"
                                  "    return sort\n\n\napp = FastAPI()\n\n\n@app.get('/x')\ndef e(v=Depends(filters)):\n"
                                  "    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:18-19", "/x", application="main.py:15",
                                   deps=[("filters", "main.py:19")])]})
        self.assertIn("query 'sort'", reminders(c))
        self.assertIn("query 'order'", reminders(c))

    def test_renamed_import_of_a_marker_alias(self):
        c = claims_of({"params.py": "from typing import Annotated\nfrom fastapi import Header\n"
                                    "Tenant = Annotated[str, Header(alias='X-Tenant')]\n",
                       "main.py": "from fastapi import FastAPI, Depends\nfrom params import Tenant as TenantHeader\n\n\n"
                                  "def dep(x: TenantHeader):\n    return x\n\n\napp = FastAPI()\n\n\n@app.get('/x')\n"
                                  "def e(v=Depends(dep)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:12-13", "/x", application="main.py:9",
                                   deps=[("dep", "main.py:13")])]})
        self.assertIn("'X-Tenant'", reminders(c))

    def test_client_kept_on_app_state(self):
        c = claims_of({"main.py": "from contextlib import asynccontextmanager\nimport httpx\nfrom fastapi import FastAPI\n\n\n"
                                  "@asynccontextmanager\nasync def lifespan(app):\n    async with httpx.AsyncClient() as wire:\n"
                                  "        app.state.wire = wire\n        yield\n\n\napp = FastAPI(lifespan=lifespan)\n",
                       "routes.py": "from fastapi import APIRouter, Request\nrouter = APIRouter()\n\n\n"
                                    "@router.get('/x')\nasync def x(request: Request):\n"
                                    "    return await request.app.state.wire.get('https://real.example')\n"})
        self.assertIn("routes.py:7", [s["at"] for s in c.suspects()])

    def test_client_at_must_bind_the_receiver_in_its_scope(self):
        c = claims_of({"h.py": "import httpx\n\n\ndef remote():\n    cache = httpx.Client()\n    return cache\n\n\n"
                               "def local():\n    cache = {'id': 7}\n    return cache.get('id')\n"})
        self.assertTrue(c.add_http({"at": "h.py:11", "library": "httpx", "method": "GET", "client_at": "h.py:5",
                                    "target": {"kind": "literal", "value": "id"}}))


class HeldOutFindings(unittest.TestCase):
    """Faults found by running the checker on repositories it was never tuned on (case_auto_hub, 08/10/2026)."""

    def test_attribute_holding_a_client_factory(self):
        # spatiumddi push.py: self._client_factory = client_factory or self._default_client; with ...() as c: c.post
        c = claims_of({"p.py": "import httpx\nclass Push:\n    def __init__(self, client_factory=None):\n"
                               "        self._client_factory = client_factory or self._default_client\n"
                               "    def _default_client(self) -> httpx.Client:\n        return httpx.Client()\n"
                               "    def send(self, body):\n        with self._client_factory() as c:\n"
                               "            return c.post('/x', json=body)\n"})
        self.assertIn("p.py:9", [s["at"] for s in c.suspects()])

    def test_getattr_with_a_runtime_method_name(self):
        # spatiumddi hetzner.py: await getattr(client, method)(path) on an httpx.AsyncClient parameter
        c = claims_of({"h.py": "import httpx\nasync def send(client: httpx.AsyncClient, method: str, path: str):\n"
                               "    return await getattr(client, method)(path)\n"
                               "def other(d: dict, key: str):\n    return getattr(d, key)()\n"})
        flagged = [s["at"] for s in c.suspects()]
        self.assertIn("h.py:3", flagged)
        self.assertNotIn("h.py:5", flagged)

    def test_http_client_module_named_but_not_called(self):
        # spatiumddi k8s.py: `import http.client`, `-> tuple[int, http.client.HTTPResponse]`, `except
        # http.client.HTTPException` are not calls; http.client.HTTPSConnection(...) is
        c = claims_of({"k.py": "import http.client\ndef f() -> http.client.HTTPResponse:\n"
                               "    conn = http.client.HTTPSConnection('k8s')\n    try:\n        conn.request('GET', '/')\n"
                               "    except http.client.HTTPException:\n        pass\n"})
        flagged = [s["at"] for s in c.suspects()]
        self.assertIn("k.py:3", flagged)
        self.assertNotIn("k.py:1", flagged)
        self.assertNotIn("k.py:2", flagged)
        self.assertNotIn("k.py:6", flagged)

    def test_factory_called_inside_an_annotated_alias(self):
        # spatiumddi: ManageUser = Annotated[User, Depends(require_permission("admin", P))]; the route line only
        # shows `u: ManageUser`, the factory's own arguments are not request parameters
        c = claims_of({"main.py": "from typing import Annotated\nfrom fastapi import FastAPI, Depends, Header\n"
                                  "def require_permission(action: str, resource_type: str):\n"
                                  "    def _dep(x_user: str = Header()):\n        return x_user\n    return _dep\n"
                                  "ManageUser = Annotated[str, Depends(require_permission('admin', 'P'))]\n"
                                  "app = FastAPI()\n@app.get('/x')\ndef e(u: ManageUser):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:9-10", "/x", application="main.py:8",
                                   deps=[("require_permission", "main.py:10")])]})
        self.assertIn("header 'x-user'", reminders(c))
        self.assertNotIn("'action'", reminders(c))

    def test_python_314_except_without_parentheses_still_parses(self):
        # PrintStash: `except TypeError, ValueError:` (PEP 758) made the file unparsable on 3.11, so every
        # dict.get( line of the file was flagged
        c = claims_of({"p.py": "import httpx\nasync def r(url):\n    async with httpx.AsyncClient() as client:\n"
                               "        body = (await client.get(url)).json()\n    try:\n        n = int(body.get('n'))\n"
                               "    except TypeError, ValueError:\n        n = 0\n    return body.get('x'), n\n"})
        flagged = [s["at"] for s in c.suspects()]
        self.assertIn("p.py:4", flagged)
        self.assertNotIn("p.py:6", flagged)
        self.assertNotIn("p.py:9", flagged)

    def test_dependency_scalar_named_in_the_route_path_is_a_path_parameter(self):
        # facet: require_share_client(album_id: int) on /api/shared/album/{album_id}/picks; the judge read the
        # packet (no route path there) as "query", so this pins what the agent itself is told
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends\ndef share(album_id: int):\n    return album_id\n"
                                  "app = FastAPI()\n@app.get('/album/{album_id}/picks')\ndef e(v=Depends(share)):\n"
                                  "    return v\n"})
        c.submit({"routes": [route("main.py::e", "main.py:5-6", "/album/{album_id}/picks", application="main.py:4",
                                   deps=[("share", "main.py:6")])]})
        self.assertIn("path 'album_id'", reminders(c))
        self.assertNotIn("query 'album_id'", reminders(c))

    def test_super_call_inside_a_client_subclass(self):
        # caura: class IdentityTokenSession(requests.Session) overriding request() and calling super().request(...)
        c = claims_of({"s.py": "import requests\nclass Signed(requests.Session):\n"
                               "    def request(self, *args, **kwargs):\n        return super().request(*args, **kwargs)\n"
                               "class Plain:\n    def get(self, k):\n        return super().get(k)\n"})
        flagged = [s["at"] for s in c.suspects()]
        self.assertIn("s.py:4", flagged)
        self.assertNotIn("s.py:7", flagged)

    def test_instance_of_a_class_uses_call_not_init(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends, Header\n\n\nclass Authentication:\n"
                                  "    def __init__(self, isAdmin: bool = False):\n        self.isAdmin = isAdmin\n\n"
                                  "    async def __call__(self, Authorization: str = Header(None)):\n        return Authorization\n\n\n"
                                  "app = FastAPI()\n\n\n@app.get('/x')\ndef e(u=Depends(Authentication())):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:15-16", "/x", application="main.py:12",
                                   deps=[("Authentication", "main.py:16")])]})
        self.assertIn("header 'Authorization'", reminders(c))
        self.assertNotIn("'isAdmin'", reminders(c))

    def test_pydantic_model_as_dependency_gives_its_scalar_fields(self):
        # case: GetPlayCaseByCaseId = Depends(): FastAPI builds the model from the query string, inherited fields too
        c = claims_of({"main.py": "from typing import Optional, Union\nfrom fastapi import FastAPI, Depends\n"
                                  "from pydantic import BaseModel, Field\n\n\nclass EnvField(BaseModel):\n"
                                  "    id: int | None = None\n    caseId: Union[int, str] = Field(...)\n"
                                  "    tags: list[str] = []\n\n\nclass FilterByEnv(EnvField):\n    host: Optional[str] = None\n\n\n"
                                  "app = FastAPI()\n\n\n@app.get('/x')\ndef e(f: FilterByEnv = Depends()):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:19-20", "/x", application="main.py:16",
                                   deps=[("FilterByEnv", "main.py:20")])]})
        for name in ("'id'", "'caseId'", "'host'"):
            self.assertIn(f"query {name}", reminders(c))
        self.assertNotIn("'tags'", reminders(c))

    def test_plain_class_without_init_declares_nothing(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends\n\n\nclass Marker:\n    level: int = 1\n\n\n"
                                  "app = FastAPI()\n\n\n@app.get('/x')\ndef e(m=Depends(Marker)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:11-12", "/x", application="main.py:8",
                                   deps=[("Marker", "main.py:12")])]})
        self.assertNotIn("'level'", reminders(c))


class RoundFive(unittest.TestCase):
    """Fifth Codex review (08/10/2026): counterexamples reproduced by running the checker and FastAPI."""

    def test_prefix_given_to_the_router_constructor_is_required(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nr = APIRouter(prefix='/v1')\n"
                                  "@r.get('/x')\ndef e():\n    return {}\napp.include_router(r)\n"})
        base = route("main.py::e", "main.py:4-5", "/x", application="main.py:2")
        self.assertTrue(c.add_route(base))
        good = dict(base, path_parts=[{"kind": "router_prefix", "value": "/v1", "at": "main.py:3"},
                                      {"kind": "decorator", "value": "/x", "at": "main.py:4"}])
        self.assertEqual(c.add_route(good), [])

    def test_router_passed_by_keyword_keeps_its_prefix(self):
        # found by the prefix mutation of the audit on AgentGPT: include_router(router=api_router, prefix="/api")
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nr = APIRouter()\n"
                                  "@r.get('/x')\ndef e():\n    return {}\napp.include_router(router=r, prefix='/api')\n"})
        base = route("main.py::e", "main.py:4-5", "/x", application="main.py:2")
        self.assertTrue(c.add_route(base))
        good = dict(base, path_parts=[{"kind": "include_prefix", "value": "/api", "at": "main.py:7"},
                                      {"kind": "decorator", "value": "/x", "at": "main.py:4"}])
        self.assertEqual(c.add_route(good), [])

    def test_config_at_must_build_the_client_called(self):
        c = claims_of({"h.py": "import httpx\nfrom types import SimpleNamespace\n"
                               "settings = SimpleNamespace(A='https://a.example', B='https://b.example')\n"
                               "a = httpx.Client(base_url=settings.A)\nb = httpx.Client(base_url=settings.B)\n"
                               "def e():\n    return a.get('/x')\n"})
        claim = {"at": "h.py:7", "library": "httpx", "method": "GET",
                 "target": {"kind": "config", "value": "settings.B", "config_at": "h.py:5"}}
        self.assertTrue(c.add_http(claim))
        self.assertEqual(c.add_http(dict(claim, target={"kind": "config", "value": "settings.A",
                                                        "config_at": "h.py:4"})), [])

    def test_same_parameter_name_keeps_the_library_of_its_function(self):
        c = claims_of({"h.py": "import httpx\nimport requests\n"
                               "def a(wire: httpx.Client):\n    return wire.get('https://a.example')\n"
                               "def b(wire: requests.Session):\n    return wire.get('https://b.example')\n"})
        self.assertEqual(http(c, "h.py:6", "requests", "GET", "https://b.example"), [])
        self.assertTrue(http(c, "h.py:6", "httpx", "GET", "https://b.example"))
        self.assertEqual(http(c, "h.py:4", "httpx", "GET", "https://a.example"), [])

    def test_client_subclass_of_another_file_keeps_its_library(self):
        # found while fixing the case above: the library came from a `client` of another function by chance
        c = claims_of({"inv.py": "import httpx\nclass InventoryClient(httpx.AsyncClient):\n    pass\n",
                       "h.py": "from inv import InventoryClient\nasync def r():\n    async with InventoryClient() as client:\n"
                               "        return await client.put('https://inv.example')\n"})
        self.assertEqual(http(c, "h.py:4", "httpx", "PUT", "https://inv.example"), [])
        self.assertTrue(http(c, "h.py:4", "aiohttp", "PUT", "https://inv.example"))

    def test_client_reached_through_a_module_import(self):
        c = claims_of({"clients.py": "import httpx\nwire = httpx.Client()\n",
                       "routes.py": "import clients\ndef e():\n    return clients.wire.get('https://real.example')\n"})
        self.assertIn("routes.py:3", [s["at"] for s in c.suspects()])
        self.assertEqual(http(c, "routes.py:3", "httpx", "GET", "https://real.example"), [])

    def test_client_from_an_imported_annotated_dependency(self):
        c = claims_of({"clients.py": "import httpx\nfrom typing import Annotated\nfrom fastapi import Depends\n"
                                     "def get_wire():\n    with httpx.Client() as c:\n        yield c\n"
                                     "Wire = Annotated[httpx.Client, Depends(get_wire)]\n",
                       "routes.py": "from fastapi import FastAPI\nfrom clients import Wire\napp = FastAPI()\n"
                                    "@app.get('/x')\ndef e(wire: Wire):\n    return wire.get('https://real.example')\n"})
        self.assertIn("routes.py:6", [s["at"] for s in c.suspects()])
        self.assertEqual(http(c, "routes.py:6", "httpx", "GET", "https://real.example"), [])

    def test_partial_dependency_reads_the_wrapped_function(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends, Header\nfrom functools import partial\n"
                                  "def check(scope, x_tenant: str = Header()):\n    return x_tenant\n"
                                  "tenant = partial(check, 'read')\napp = FastAPI()\n"
                                  "@app.get('/x')\ndef e(v=Depends(tenant)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:7-8", "/x", application="main.py:6",
                                   deps=[("tenant", "main.py:8")])]})
        self.assertIn("header 'x-tenant'", reminders(c))
        self.assertNotIn("'scope'", reminders(c))  # bound by partial, not a request parameter

    def test_annotated_depends_without_argument_inside_a_dependency(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends\nfrom typing import Annotated\n"
                                  "class Filters:\n    def __init__(self, q: str = ''):\n        self.q = q\n"
                                  "def outer(f: Annotated[Filters, Depends()]):\n    return f\napp = FastAPI()\n"
                                  "@app.get('/x')\ndef e(v=Depends(outer)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:9-10", "/x", application="main.py:8",
                                   deps=[("outer", "main.py:10")])]})
        self.assertIn("query 'q'", reminders(c))


class RoundSix(unittest.TestCase):
    """Sixth Codex review (08/10/2026): counterexamples reproduced by running the checker and FastAPI."""

    def test_prefixes_must_come_in_the_order_they_apply(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nr = APIRouter(prefix='/v1')\n"
                                  "@r.get('/x')\ndef e():\n    return {}\napp.include_router(r, prefix='/api')\n"})
        base = route("main.py::e", "main.py:4-5", "/x", application="main.py:2")
        api = {"kind": "include_prefix", "value": "/api", "at": "main.py:7"}
        v1 = {"kind": "router_prefix", "value": "/v1", "at": "main.py:3"}
        x = {"kind": "decorator", "value": "/x", "at": "main.py:4"}
        self.assertTrue(c.add_route(dict(base, path_parts=[v1, api, x])))  # /v1/api/x
        self.assertEqual(c.add_route(dict(base, path_parts=[api, v1, x])), [])  # /api/v1/x

    def test_unused_attach_helper_does_not_switch_off_the_prefix_check(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nr = APIRouter()\n"
                                  "@r.get('/x')\ndef e():\n    return {}\napp.include_router(r, prefix='/api')\n"
                                  "def attach(target, router):\n    target.include_router(router)\n"})
        self.assertTrue(c.add_route(route("main.py::e", "main.py:4-5", "/x", application="main.py:2")))

    def test_include_on_an_attribute_is_not_read_as_missing(self):
        # found while fixing the case above: self.app.include_router(r) was skipped, so r looked unregistered
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nr = APIRouter()\n"
                                  "@r.get('/x')\ndef e():\n    return {}\nclass Builder:\n    def __init__(self, app):\n"
                                  "        self.app = app\n    def build(self):\n        self.app.include_router(r)\n"
                                  "Builder(app).build()\n"})
        self.assertEqual(c.add_route(route("main.py::e", "main.py:4-5", "/x", application="main.py:2")), [])

    def test_absolute_url_overrides_the_configured_base_url(self):
        c = claims_of({"h.py": "import httpx\nfrom types import SimpleNamespace\n"
                               "settings = SimpleNamespace(URL='https://base.example')\n"
                               "c = httpx.Client(base_url=settings.URL)\ndef e():\n    return c.get('https://other.example/x')\n"})
        claim = {"at": "h.py:6", "library": "httpx", "method": "GET",
                 "target": {"kind": "config", "value": "settings.URL", "config_at": "h.py:4"}}
        self.assertTrue(c.add_http(claim))
        self.assertEqual(http(c, "h.py:6", "httpx", "GET", "https://other.example/x"), [])

    def test_attribute_client_of_another_class(self):
        c = claims_of({"h.py": "import httpx\nclass Remote:\n    def __init__(self):\n        self.client = httpx.Client()\n"
                               "class Cache:\n    def __init__(self):\n        self.client = {'id': 1}\n"
                               "    def e(self):\n        return self.client.get('id')\n"
                               "    def r(self):\n        return Remote().client.get('https://a.example')\n"})
        self.assertNotIn("h.py:9", [s["at"] for s in c.suspects()])
        self.assertTrue(http(c, "h.py:9", "httpx", "GET", "id"))

    def test_attribute_claim_in_a_file_without_http_library(self):
        # found by the gold audit (token-proxy): the class-scoped check crashed on a file the scan skips early
        c = claims_of({"h.py": "class A:\n    def e(self):\n        return self.store.get('https://a.example')\n"})
        self.assertTrue(http(c, "h.py:3", "httpx", "GET", "https://a.example"))

    def test_client_re_exported_by_a_package(self):
        c = claims_of({"infra/transport.py": "import httpx\nwire = httpx.Client()\n",
                       "infra/__init__.py": "from .transport import wire\n",
                       "routes.py": "from infra import wire\ndef e():\n    return wire.get('https://real.example')\n"})
        self.assertIn("routes.py:3", [s["at"] for s in c.suspects()])
        self.assertEqual(http(c, "routes.py:3", "httpx", "GET", "https://real.example"), [])

    def test_inherited_constructor_of_a_class_dependency(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends, Header\nclass Base:\n"
                                  "    def __init__(self, x_tenant: str = Header()):\n        self.x_tenant = x_tenant\n"
                                  "class Tenant(Base):\n    pass\napp = FastAPI()\n"
                                  "@app.get('/x')\ndef e(v=Depends(Tenant)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:8-9", "/x", application="main.py:7",
                                   deps=[("Tenant", "main.py:9")])]})
        self.assertIn("header 'x-tenant'", reminders(c))

    def test_pydantic_field_alias_is_the_query_name(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends\nfrom pydantic import BaseModel, Field\n"
                                  "class Filters(BaseModel):\n    sort_by: str = Field('name', alias='sortBy')\napp = FastAPI()\n"
                                  "@app.get('/x')\ndef e(v=Depends(Filters)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:6-7", "/x", application="main.py:5",
                                   deps=[("Filters", "main.py:7")])]})
        self.assertIn("query 'sortBy'", reminders(c))
        self.assertNotIn("'sort_by'", reminders(c))

    def test_partial_keyword_stays_a_parameter(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends\nfrom functools import partial\n"
                                  "def filters(limit: int = 10):\n    return limit\ntenant = partial(filters, limit=20)\n"
                                  "app = FastAPI()\n@app.get('/x')\ndef e(v=Depends(tenant)):\n    return v\n"})
        c.submit({"routes": [route("main.py::e", "main.py:7-8", "/x", application="main.py:6",
                                   deps=[("tenant", "main.py:8")])]})
        self.assertIn("query 'limit'", reminders(c))


def part(kind, value, at):
    return {"kind": kind, "value": value, "at": at}


class RoundSeven(unittest.TestCase):
    """Seventh review (a Claude agent, 08/10/2026, stopped by a rate limit; its probes were rerun here)."""

    def test_called_helper_including_another_router_keeps_the_prefix_check(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\nfrom setup import register\napp = FastAPI()\n"
                                  "r = APIRouter()\n@r.get('/x')\ndef e():\n    return {}\napp.include_router(r, prefix='/api')\n"
                                  "register(app)\n",
                       "setup.py": "from fastapi import APIRouter\nother = APIRouter()\ndef register(target):\n"
                                   "    target.include_router(other, prefix='/o')\n"})
        self.assertTrue(c.add_route(route("main.py::e", "main.py:5-6", "/x", application="main.py:3")))

    def test_prefix_parts_must_be_the_ones_on_the_way(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nr = APIRouter()\nadmin = APIRouter()\n"
                                  "@r.get('/x')\ndef e():\n    return {}\napp.include_router(r, prefix='/api')\n"
                                  "app.include_router(admin, prefix='/admin')\n"})
        base = route("main.py::e", "main.py:5-6", "/x", application="main.py:2")
        x = part("decorator", "/x", "main.py:5")
        api = part("include_prefix", "/api", "main.py:8")
        self.assertTrue(c.add_route(dict(base, path_parts=[part("include_prefix", "/admin", "main.py:9"), api, x])))
        self.assertTrue(c.add_route(dict(base, path_parts=[api, api, x])))
        self.assertEqual(c.add_route(dict(base, path_parts=[api, x])), [])

    def test_prefix_value_must_be_the_literal_given(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\n"
                                  "r = APIRouter(prefix='/auth', tags=['authentication'])\n@r.post('/login')\ndef login():\n"
                                  "    return {}\napp.include_router(r, prefix='/api/v1', tags=['v1'])\n"})
        base = route("main.py::login", "main.py:4-5", "/login", method="POST", application="main.py:2")
        login = part("decorator", "/login", "main.py:4")
        self.assertTrue(c.add_route(dict(base, path_parts=[part("include_prefix", "v1", "main.py:7"),
                                                           part("router_prefix", "authentication", "main.py:3"), login])))
        self.assertEqual(c.add_route(dict(base, path_parts=[part("include_prefix", "/api/v1", "main.py:7"),
                                                            part("router_prefix", "/auth", "main.py:3"), login])), [])

    def test_router_subclass_and_renamed_import_are_routers(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nclass Slash(APIRouter):\n"
                                  "    pass\nr = Slash()\n@r.get('/x')\ndef e():\n    return {}\napp.include_router(r)\n"})
        self.assertEqual(c._decorator_problems(("main.py", 6, 7), "main.py::e", "GET"), [])
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter as Router\napp = FastAPI()\nr = Router()\n"
                                  "@r.get('/x')\ndef e():\n    return {}\napp.include_router(r)\n"})
        self.assertEqual(c._decorator_problems(("main.py", 4, 5), "main.py::e", "GET"), [])

    def test_dependency_used_by_the_handler_but_not_declared(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends, Header\ndef verify(x_token: str = Header()):\n"
                                  "    return x_token\napp = FastAPI()\n@app.get('/x')\ndef e(v=Depends(verify)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:5-6", "/x", application="main.py:4", deps=[])]})
        self.assertIn("verify", reminders(c))

    def test_dependency_name_must_be_the_depends_target(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends, Header\nclass Session:\n    pass\n"
                                  "def get_db(x_tenant: str = Header()):\n    return Session()\n"
                                  "app = FastAPI()\n@app.get('/x')\ndef e(db: Session = Depends(get_db)):\n    return {}\n"})
        self.assertFalse(c.dependency_at("db", ("main.py", 8, 8)))
        self.assertFalse(c.dependency_at("Session", ("main.py", 8, 8)))
        self.assertTrue(c.dependency_at("get_db", ("main.py", 8, 8)))

    def test_config_key_must_be_a_whole_name_of_the_url(self):
        c = claims_of({"h.py": "import httpx\nfrom types import SimpleNamespace\n"
                               "settings = SimpleNamespace(PAYMENT_API_URL='https://pay.example')\n"
                               "def e():\n    return httpx.get(settings.PAYMENT_API_URL + '/charge')\n"})
        claim = lambda v: c.add_http({"at": "h.py:5", "library": "httpx", "method": "GET",  # noqa: E731
                                      "target": {"kind": "config", "value": v}})
        for wrong in ("API_URL", "settings", "e"):
            self.assertTrue(claim(wrong), wrong)
        self.assertEqual(claim("settings.PAYMENT_API_URL"), [])
        self.assertEqual(claim("PAYMENT_API_URL"), [])

    def test_config_at_of_the_same_attribute_in_another_class(self):
        c = claims_of({"h.py": "import httpx\nfrom types import SimpleNamespace\n"
                               "settings = SimpleNamespace(USERS='https://u.example', ORDERS='https://o.example')\n"
                               "class Users:\n    def __init__(self):\n        self.client = httpx.Client(base_url=settings.USERS)\n"
                               "    def me(self):\n        return self.client.get('/me')\n"
                               "class Orders:\n    def __init__(self):\n        self.client = httpx.Client(base_url=settings.ORDERS)\n"})
        claim = lambda v, at: c.add_http({"at": "h.py:8", "library": "httpx", "method": "GET",  # noqa: E731
                                          "target": {"kind": "config", "value": v, "config_at": at}})
        self.assertTrue(claim("settings.ORDERS", "h.py:11"))
        self.assertEqual(claim("settings.USERS", "h.py:6"), [])

    def test_client_returned_by_a_method_and_used_in_place(self):
        c = claims_of({"h.py": "import httpx\nclass Api:\n    def _client(self):\n        return httpx.Client(base_url='https://a.example')\n"
                               "    def me(self):\n        return self._client().get('/me')\n"})
        self.assertIn("h.py:6", [s["at"] for s in c.suspects()])


class RoundSevenCodex(unittest.TestCase):
    """Seventh Codex review (08/10/2026): counterexamples reproduced by running the checker and FastAPI."""

    def test_include_runs_before_the_inner_router_is_filled(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nouter = APIRouter()\n"
                                  "inner = APIRouter()\n@inner.get('/x')\ndef e():\n    return {}\n"
                                  "app.include_router(outer)\nouter.include_router(inner)\n"})
        self.assertTrue(c.add_route(route("main.py::e", "main.py:5-6", "/x", application="main.py:2")))
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nouter = APIRouter()\n"
                                  "inner = APIRouter()\n@inner.get('/x')\ndef e():\n    return {}\n"
                                  "outer.include_router(inner)\napp.include_router(outer)\n"})
        self.assertEqual(c.add_route(route("main.py::e", "main.py:5-6", "/x", application="main.py:2")), [])

    def test_route_on_the_second_of_two_decorators(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nother = FastAPI()\n"
                                  "a = APIRouter()\nb = APIRouter()\n@a.get('/x')\n@b.get('/x')\ndef e():\n    return {}\n"
                                  "app.include_router(a)\nother.include_router(b)\n"})
        self.assertEqual(c.add_route(route("main.py::e", "main.py:6-8", "/x", application="main.py:3")), [])

    def test_json_of_a_response_is_not_a_client(self):
        c = claims_of({"h.py": "import httpx\ndef e():\n    data = httpx.Client().get('https://real.example').json()\n"
                               "    return data.get('id')\n"})
        self.assertNotIn("h.py:4", [s["at"] for s in c.suspects()])
        self.assertTrue(http(c, "h.py:4", "httpx", "GET", "id"))

    def test_result_of_a_helper_given_the_client_is_not_a_client(self):
        # found while fixing the case above (primer, caura): pr = await fetch(url, http); pr.get(...) is a dict
        c = claims_of({"h.py": "import httpx\nasync def fetch(url, http):\n    return (await http.get(url)).json()\n"
                               "async def e(url):\n    async with httpx.AsyncClient() as http:\n"
                               "        pr = await fetch(url, http)\n        return pr.get('servers')\n"})
        self.assertNotIn("h.py:7", [s["at"] for s in c.suspects()])

    def test_client_method_handed_to_a_thread(self):
        c = claims_of({"h.py": "import asyncio\nimport httpx\nc = httpx.Client()\n"
                               "async def e():\n    return await asyncio.to_thread(c.get, 'https://real.example')\n"})
        self.assertIn("h.py:5", [s["at"] for s in c.suspects()])

    def test_client_behind_a_property(self):
        c = claims_of({"h.py": "import httpx\nclass API:\n    def __init__(self):\n        self._wire = httpx.Client()\n"
                               "    @property\n    def transport(self):\n        return self._wire\n"
                               "    def e(self):\n        return self.transport.get('https://real.example')\n"})
        self.assertIn("h.py:9", [s["at"] for s in c.suspects()])
        self.assertEqual(http(c, "h.py:9", "httpx", "GET", "https://real.example"), [])

    def test_query_parameter_model(self):
        c = claims_of({"main.py": "from typing import Annotated\nfrom fastapi import FastAPI, Depends, Query\n"
                                  "from pydantic import BaseModel\nclass Filters(BaseModel):\n    q: str = ''\n"
                                  "def dep(f: Annotated[Filters, Query()]):\n    return f\napp = FastAPI()\n"
                                  "@app.get('/x')\ndef e(v=Depends(dep)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:9-10", "/x", application="main.py:8",
                                   deps=[("dep", "main.py:10")])]})
        self.assertIn("query 'q'", reminders(c))
        self.assertNotIn("'f'", reminders(c))

    def test_nested_dependency_given_by_keyword(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends, Header\ndef inner(x_tenant: str = Header()):\n"
                                  "    return x_tenant\ndef dep(v=Depends(dependency=inner)):\n    return v\napp = FastAPI()\n"
                                  "@app.get('/x')\ndef e(v=Depends(dep)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:7-8", "/x", application="main.py:6",
                                   deps=[("dep", "main.py:8")])]})
        self.assertIn("header 'x-tenant'", reminders(c))

    def test_renamed_marker_import(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends, Header as H\ndef dep(x_tenant: str = H()):\n"
                                  "    return x_tenant\napp = FastAPI()\n@app.get('/x')\ndef e(v=Depends(dep)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:5-6", "/x", application="main.py:4",
                                   deps=[("dep", "main.py:6")])]})
        self.assertIn("header 'x-tenant'", reminders(c))
        self.assertNotIn("query 'x_tenant'", reminders(c))


class RoundEight(unittest.TestCase):
    """Eighth Codex review (08/10/2026): counterexamples reproduced by running the checker and FastAPI."""

    def test_router_prefix_inside_an_app_factory(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\ndef create_app():\n    app = FastAPI()\n"
                                  "    r = APIRouter(prefix='/api')\n    @r.get('/x')\n    def e():\n        return {}\n"
                                  "    app.include_router(r)\n    return app\napp = create_app()\n"})
        base = route("main.py::e", "main.py:5-6", "/x", application="main.py:3")
        self.assertTrue(c.add_route(base))
        self.assertEqual(c.add_route(dict(base, path_parts=[part("router_prefix", "/api", "main.py:4"),
                                                            part("decorator", "/x", "main.py:5")])), [])

    def test_client_attribute_copied_to_a_local(self):
        c = claims_of({"h.py": "import httpx\nclass API:\n    def __init__(self):\n        self._wire = httpx.Client()\n"
                               "    def e(self):\n        wire = self._wire\n        return wire.get('https://real.example')\n"})
        self.assertIn("h.py:7", [s["at"] for s in c.suspects()])
        self.assertEqual(http(c, "h.py:7", "httpx", "GET", "https://real.example"), [])

    def test_container_of_clients_is_not_a_client(self):
        c = claims_of({"h.py": "import httpx\ndef e(clients: dict[str, httpx.Client]):\n    return clients.get('primary')\n"})
        self.assertNotIn("h.py:3", [s["at"] for s in c.suspects()])
        self.assertTrue(http(c, "h.py:3", "httpx", "GET", "primary"))

    def test_bound_method_kept_on_the_instance(self):
        c = claims_of({"h.py": "import httpx\nclass API:\n    def __init__(self):\n        self._wire = httpx.Client()\n"
                               "        self.fetch = self._wire.get\n    def e(self):\n"
                               "        return self.fetch('https://real.example')\n"})
        self.assertIn("h.py:7", [s["at"] for s in c.suspects()])
        self.assertEqual(http(c, "h.py:7", "httpx", "GET", "https://real.example"), [])

    def test_claim_on_a_method_handed_to_a_thread(self):
        c = claims_of({"h.py": "import asyncio\nimport httpx\nc = httpx.Client()\n"
                               "async def e():\n    return await asyncio.to_thread(c.get, 'https://real.example')\n"})
        self.assertEqual(http(c, "h.py:5", "httpx", "GET", "https://real.example"), [])
        self.assertTrue(http(c, "h.py:5", "httpx", "POST", "https://real.example"))

    def test_query_model_list_field(self):
        c = claims_of({"main.py": "from typing import Annotated\nfrom fastapi import FastAPI, Depends, Query\n"
                                  "from pydantic import BaseModel\nclass Filters(BaseModel):\n    tags: list[str] = []\n"
                                  "def dep(f: Annotated[Filters, Query()]):\n    return f\napp = FastAPI()\n"
                                  "@app.get('/x')\ndef e(v=Depends(dep)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:9-10", "/x", application="main.py:8",
                                   deps=[("dep", "main.py:10")])]})
        self.assertIn("query 'tags'", reminders(c))

    def test_model_alias_generator(self):
        c = claims_of({"main.py": "from typing import Annotated\nfrom fastapi import FastAPI, Depends, Query\n"
                                  "from pydantic import BaseModel, ConfigDict\nfrom pydantic.alias_generators import to_camel\n"
                                  "class Filters(BaseModel):\n    model_config = ConfigDict(alias_generator=to_camel)\n"
                                  "    sort_by: str = ''\ndef dep(f: Annotated[Filters, Query()]):\n    return f\n"
                                  "app = FastAPI()\n@app.get('/x')\ndef e(v=Depends(dep)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:11-12", "/x", application="main.py:10",
                                   deps=[("dep", "main.py:12")])]})
        self.assertIn("query 'sortBy'", reminders(c))
        self.assertNotIn("'sort_by'", reminders(c))

    def test_instance_with_an_inherited_call(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends, Header\nclass Base:\n"
                                  "    def __call__(self, x_tenant: str = Header()):\n        return x_tenant\n"
                                  "class Tenant(Base):\n    pass\ntenant = Tenant()\napp = FastAPI()\n"
                                  "@app.get('/x')\ndef e(v=Depends(tenant)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:9-10", "/x", application="main.py:8",
                                   deps=[("tenant", "main.py:10")])]})
        self.assertIn("header 'x-tenant'", reminders(c))


class RoundNine(unittest.TestCase):
    """Ninth review (a Claude agent, 09/10/2026, stopped by a rate limit; its notes and probes were rerun here)."""

    def test_router_module_imported_relatively(self):
        c = claims_of({"app/items.py": "from fastapi import APIRouter\nrouter = APIRouter(prefix='/items')\n"
                                       "@router.get('/list')\ndef ls():\n    return []\n",
                       "app/main.py": "from fastapi import FastAPI\nfrom . import items\napp = FastAPI()\n"
                                      "app.include_router(items.router)\n"})
        base = route("app/items.py::ls", "app/items.py:3-4", "/list", application="app/main.py:3")
        self.assertTrue(c.add_route(base))

    def test_dict_attribute_with_annotation_is_not_a_client(self):
        # xianyu qr_login.py: self.sessions: Dict[str, QRLoginSession] = {}; self.sessions.get(k)
        c = claims_of({"q.py": "import aiohttp\nclass Q:\n    def __init__(self):\n        self.sessions: dict = {}\n"
                               "    def g(self, k):\n        return self.sessions.get(k)\n"})
        self.assertNotIn("q.py:6", [s["at"] for s in c.suspects()])

    def test_client_method_chosen_by_a_condition(self):
        # xianyu notification_dispatcher.py: request = session.post if m == 'POST' else session.put
        c = claims_of({"n.py": "import aiohttp\nasync def send(url, m):\n    async with aiohttp.ClientSession() as session:\n"
                               "        request = session.post if m == 'POST' else session.put\n"
                               "        async with request(url) as r:\n            return r.status\n"})
        self.assertIn("n.py:5", [s["at"] for s in c.suspects()])

    def test_library_reached_through_another_module(self):
        # xianyu cookie mixin: self.session = _host.aiohttp.ClientSession(...)
        c = claims_of({"host.py": "import aiohttp\n",
                       "m.py": "import host as _host\nclass M:\n    async def f(self):\n"
                               "        self.session = _host.aiohttp.ClientSession()\n"
                               "        return await self.session.get('https://x.example')\n"})
        self.assertIn("m.py:5", [s["at"] for s in c.suspects()])

    def test_attribute_named_like_a_library_is_not_the_library(self):
        # found while fixing the case above (shortlist): report.requests.warnings, "assistant.requests.send"
        c = claims_of({"r.py": "def persist(session, report, job_id):\n    scope = 'assistant.requests.send'\n"
                               "    if report.requests.warnings:\n        return session.get(object, job_id)\n"})
        self.assertNotIn("r.py:4", [s["at"] for s in c.suspects()])

    def test_mixin_using_a_client_its_subclass_creates(self):
        # xianyu: XianyuLive(TokenMixin, ...) sets self.session = aiohttp.ClientSession(); the mixin posts on it
        c = claims_of({"mixin.py": "class TokenMixin:\n    async def t(self):\n"
                                   "        return await self.session.post('https://x.example')\n",
                       "main.py": "import aiohttp\nfrom mixin import TokenMixin\nclass Bot(TokenMixin):\n"
                                  "    def __init__(self):\n        self.session = aiohttp.ClientSession()\n"})
        self.assertIn("mixin.py:3", [s["at"] for s in c.suspects()])

    def test_project_module_named_like_an_http_library(self):
        # found while fixing the case above (PrintStash): `from . import requests` is the project's module
        c = claims_of({"app/requests.py": "def identity_scheme(r):\n    return r\n",
                       "app/jobs.py": "from . import requests\nfrom .requests import identity_scheme\n"
                                      "def cancel(session, job_id):\n    return session.get(object, job_id)\n"})
        self.assertNotIn("app/jobs.py:4", [s["at"] for s in c.suspects()])

    def test_routers_included_in_a_loop(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nitems = APIRouter(prefix='/items')\n"
                                  "users = APIRouter()\n@items.get('/list')\ndef ls():\n    return []\n"
                                  "for r in (items, users):\n    app.include_router(r, prefix='/api')\n"})
        base = route("main.py::ls", "main.py:5-6", "/list", application="main.py:2")
        self.assertTrue(c.add_route(base))
        self.assertEqual(c.add_route(dict(base, path_parts=[part("include_prefix", "/api", "main.py:9"),
                                                            part("router_prefix", "/items", "main.py:3"),
                                                            part("decorator", "/list", "main.py:5")])), [])

    def test_router_level_dependency_not_declared(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter, Depends, Header\n"
                                  "def token(x_token: str = Header()):\n    return x_token\napp = FastAPI()\n"
                                  "r = APIRouter(dependencies=[Depends(token)])\n@r.get('/x')\ndef e():\n    return {}\n"
                                  "app.include_router(r)\n"})
        c.submit({"routes": [route("main.py::e", "main.py:6-7", "/x", application="main.py:4", deps=[])]})
        self.assertIn("token", reminders(c))

    def test_alias_dependency_not_declared(self):
        c = claims_of({"main.py": "from typing import Annotated\nfrom fastapi import FastAPI, Depends\n"
                                  "def pagination(page: int = 1):\n    return page\nPageDep = Annotated[int, Depends(pagination)]\n"
                                  "app = FastAPI()\n@app.get('/x')\ndef e(p: PageDep):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:7-8", "/x", application="main.py:6", deps=[])]})
        self.assertIn("pagination", reminders(c))

    def test_client_from_app_state_through_an_untyped_provider(self):
        c = claims_of({"main.py": "import httpx\nfrom fastapi import FastAPI\nasync def lifespan(app):\n"
                                  "    app.state.http = httpx.AsyncClient()\n    yield\napp = FastAPI(lifespan=lifespan)\n",
                       "deps.py": "def get_http(request):\n    return request.app.state.http\n",
                       "routes.py": "from fastapi import APIRouter, Depends\nfrom deps import get_http\nr = APIRouter()\n"
                                    "@r.get('/x')\nasync def e(client=Depends(get_http)):\n"
                                    "    return await client.get('https://real.example/x')\n"})
        self.assertIn("routes.py:6", [s["at"] for s in c.suspects()])

    def test_same_name_bound_to_another_client_kind_in_another_function(self):
        c = claims_of({"h.py": "import httpx\nimport redis\ndef a():\n    client = httpx.Client()\n"
                               "    return client.get('https://a.example')\ndef b():\n    client = redis.Redis()\n"
                               "    return client.get('key')\n"})
        self.assertEqual(http(c, "h.py:5", "httpx", "GET", "https://a.example"), [])
        self.assertTrue(http(c, "h.py:8", "httpx", "GET", "key"))

    def test_client_attribute_set_by_a_base_class_of_another_file(self):
        c = claims_of({"base.py": "import httpx\nclass BaseAPI:\n    def __init__(self):\n        self._client = httpx.AsyncClient()\n",
                       "github.py": "from base import BaseAPI\nclass GitHub(BaseAPI):\n    async def me(self):\n"
                                    "        return await self._client.get('https://api.github.com/user')\n"})
        self.assertIn("github.py:4", [s["at"] for s in c.suspects()])

    def test_dotted_dependency_defined_in_two_modules(self):
        dep = "from fastapi import Header\ndef common(x_{v}: str = Header()):\n    return x_{v}\n"
        c = claims_of({"api/v1/deps.py": dep.format(v="tenant"), "api/v2/deps.py": dep.format(v="other"),
                       "api/v1/routes.py": "from fastapi import FastAPI, Depends\nfrom api.v1 import deps\napp = FastAPI()\n"
                                           "@app.get('/x')\ndef e(v=Depends(deps.common)):\n    return {}\n"})
        c.submit({"routes": [route("api/v1/routes.py::e", "api/v1/routes.py:4-5", "/x", application="api/v1/routes.py:3",
                                   deps=[("deps.common", "api/v1/routes.py:5")])]})
        self.assertIn("header 'x-tenant'", reminders(c))
        self.assertNotIn("x-other", reminders(c))


class RoundNineCodex(unittest.TestCase):
    """Ninth Codex review (09/10/2026): counterexamples reproduced by running the checker and FastAPI."""

    def test_include_in_a_branch_that_never_runs(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nr = APIRouter()\n"
                                  "@r.get('/x')\ndef e():\n    return {}\nENABLE_API = False\nif ENABLE_API:\n"
                                  "    app.include_router(r)\n"})
        self.assertTrue(c.add_route(route("main.py::e", "main.py:4-5", "/x", application="main.py:2")))

    def test_annotated_module_client_keeps_its_library(self):
        c = claims_of({"h.py": "import httpx\nimport requests\nwire: httpx.Client = httpx.Client()\n"
                               "def e():\n    return wire.get('https://example.org/x')\n"})
        self.assertTrue(http(c, "h.py:5", "requests", "GET", "https://example.org/x"))
        self.assertEqual(http(c, "h.py:5", "httpx", "GET", "https://example.org/x"), [])

    def test_client_provider_given_by_keyword(self):
        c = claims_of({"main.py": "import httpx\nfrom fastapi import FastAPI, Depends\ndef provide():\n"
                                  "    return httpx.Client()\napp = FastAPI()\n@app.get('/x')\n"
                                  "def e(wire=Depends(dependency=provide)):\n    return wire.get('https://example.org/x').json()\n"})
        self.assertIn("main.py:8", [s["at"] for s in c.suspects()])
        self.assertEqual(http(c, "main.py:8", "httpx", "GET", "https://example.org/x"), [])

    def test_client_taken_out_of_a_dict(self):
        c = claims_of({"h.py": "import httpx\nclients = {'primary': httpx.Client()}\n"
                               "def e():\n    return clients['primary'].get('https://example.org/x')\n"})
        self.assertIn("h.py:4", [s["at"] for s in c.suspects()])
        self.assertEqual(http(c, "h.py:4", "httpx", "GET", "https://example.org/x"), [])

    def test_partial_only_builds_the_call(self):
        c = claims_of({"h.py": "from functools import partial\nimport httpx\nwire = httpx.Client()\n"
                               "def e():\n    return partial(wire.get, 'https://example.org/x')\n"})
        self.assertTrue(http(c, "h.py:5", "httpx", "GET", "https://example.org/x"))

    def test_scalar_type_alias(self):
        c = claims_of({"main.py": "from typing import Annotated\nfrom uuid import UUID\nfrom fastapi import FastAPI, Depends\n"
                                  "from pydantic import Field\nUserId = UUID\nPage = Annotated[int, Field(ge=1)]\n"
                                  "def dep(user_id: UserId, page: Page = 1):\n    return user_id\napp = FastAPI()\n"
                                  "@app.get('/x')\ndef e(v=Depends(dep)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:10-11", "/x", application="main.py:9",
                                   deps=[("dep", "main.py:11")])]})
        self.assertIn("query 'user_id'", reminders(c))
        self.assertIn("query 'page'", reminders(c))

    def test_path_converter_names_a_path_parameter(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends\ndef dep(item_id: int):\n    return item_id\n"
                                  "app = FastAPI()\n@app.get('/items/{item_id:int}')\ndef e(v=Depends(dep)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:5-6", "/items/{item_id:int}", application="main.py:4",
                                   deps=[("dep", "main.py:6")])]})
        self.assertIn("path 'item_id'", reminders(c))
        self.assertNotIn("query 'item_id'", reminders(c))


class RoundTen(unittest.TestCase):
    """Tenth Codex review (09/10/2026): counterexamples reproduced by running the checker and FastAPI."""

    def test_partial_line_is_not_a_suspect(self):
        c = claims_of({"h.py": "from functools import partial\nimport httpx\nwire = httpx.Client()\n"
                               "def e():\n    return partial(wire.get, 'https://example.org/x')\n"})
        self.assertNotIn("h.py:5", [s["at"] for s in c.suspects()])

    def test_routers_listed_in_a_variable(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, APIRouter\napp = FastAPI()\nr = APIRouter(prefix='/items')\n"
                                  "@r.get('/x')\ndef e():\n    return {}\nrouters = [r]\nfor router in routers:\n"
                                  "    app.include_router(router, prefix='/api')\n"})
        self.assertTrue(c.add_route(route("main.py::e", "main.py:4-5", "/x", application="main.py:2")))

    def test_parameter_shadowing_a_module_client(self):
        c = claims_of({"h.py": "import httpx\nwire = httpx.Client()\ndef e(wire):\n    return wire.get('https://example.org/x')\n"})
        self.assertTrue(http(c, "h.py:4", "httpx", "GET", "https://example.org/x"))

    def test_client_entered_on_an_exit_stack(self):
        c = claims_of({"h.py": "import httpx\nfrom contextlib import AsyncExitStack\nasync def e():\n"
                               "    async with AsyncExitStack() as stack:\n"
                               "        wire = await stack.enter_async_context(httpx.AsyncClient())\n"
                               "        return await wire.get('https://example.org/x')\n"})
        self.assertIn("h.py:6", [s["at"] for s in c.suspects()])
        self.assertEqual(http(c, "h.py:6", "httpx", "GET", "https://example.org/x"), [])

    def test_client_provider_configured_with_partial(self):
        c = claims_of({"main.py": "from functools import partial\nimport httpx\nfrom fastapi import FastAPI, Depends\n"
                                  "def provide(base_url):\n    return httpx.Client(base_url=base_url)\n"
                                  "get_client = partial(provide, base_url='https://example.org')\napp = FastAPI()\n"
                                  "@app.get('/x')\ndef e(wire=Depends(get_client)):\n"
                                  "    return {'status': wire.get('https://example.org/x').status_code}\n"})
        self.assertIn("main.py:10", [s["at"] for s in c.suspects()])

    def test_marker_alias_given_by_a_constant(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends, Query\nPAGE = 'pageSize'\n"
                                  "def dep(page_size: int = Query(10, alias=PAGE)):\n    return page_size\napp = FastAPI()\n"
                                  "@app.get('/x')\ndef e(v=Depends(dep)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:6-7", "/x", application="main.py:5",
                                   deps=[("dep", "main.py:7")])]})
        self.assertIn("query 'pageSize'", reminders(c))
        self.assertNotIn("'page_size'", reminders(c))

    def test_marker_reused_through_a_variable(self):
        c = claims_of({"main.py": "from fastapi import FastAPI, Depends, Header\ntenant_header = Header(alias='X-Tenant')\n"
                                  "def dep(tenant: str = tenant_header):\n    return tenant\napp = FastAPI()\n"
                                  "@app.get('/x')\ndef e(v=Depends(dep)):\n    return {}\n"})
        c.submit({"routes": [route("main.py::e", "main.py:6-7", "/x", application="main.py:5",
                                   deps=[("dep", "main.py:7")])]})
        self.assertIn("header 'X-Tenant'", reminders(c))
        self.assertNotIn("query 'tenant'", reminders(c))


class RoundThreeLeftovers(unittest.TestCase):
    """Forms Codex round 3 listed as still missed by the suspect scan."""

    def test_bound_method_and_getattr(self):
        c = claims_of({"h.py": "import httpx\nwire = httpx.Client()\nfetch = wire.get\n\n\ndef a():\n"
                               "    return fetch('https://a.example')\n\n\ndef b():\n"
                               "    return getattr(wire, 'get')('https://b.example')\n"})
        flagged = [s["at"] for s in c.suspects()]
        self.assertIn("h.py:7", flagged)
        self.assertIn("h.py:11", flagged)

    def test_claims_on_renamed_and_bound_functions(self):
        c = claims_of({"h.py": "import httpx\nfrom requests import post as send_it\nwire = httpx.Client()\nfetch = wire.get\n"
                               "fetch('https://a.example')\nsend_it('https://b.example')\n"})
        self.assertEqual(http(c, "h.py:5", "httpx", "GET", "https://a.example"), [])
        self.assertTrue(http(c, "h.py:5", "httpx", "POST", "https://a.example"))
        self.assertEqual(http(c, "h.py:6", "requests", "POST", "https://b.example"), [])
        self.assertTrue(http(c, "h.py:6", "httpx", "POST", "https://b.example"))


if __name__ == "__main__":
    unittest.main()
