"""FR-029: regression tests for the five scoped implementation tasks."""
import json
import unittest

from test_extract import facts_of, kind, val
from test_render import run_on, block, validate_openapi


class FR029(unittest.TestCase):
    def test_test_routes_and_test_registration_are_excluded(self):
        fs = facts_of({
            'routes.py': 'from fastapi import APIRouter\nr=APIRouter()\n@r.get("/real")\ndef real(): pass\n',
            'main.py': 'from fastapi import FastAPI\nfrom routes import r\napp=FastAPI()\napp.include_router(r)\n',
            'tests/conftest.py': 'from fastapi import FastAPI\nfrom routes import r\napp=FastAPI()\napp.include_router(r)\n@app.get("/fake")\ndef fake(): pass\n'})
        routes = kind(fs, 'route')
        self.assertEqual(len(routes), 1)
        self.assertEqual(val(routes[0], 'path'), '/real')
        self.assertNotIn('tests/', val(routes[0], 'registration_context'))

    def test_non_decorator_routes_are_reported_individually(self):
        src = 'from fastapi import FastAPI\napp=FastAPI()\napp.add_api_route("/a", handler)\napp.add_websocket_route("/b", handler)\n'
        fs = facts_of({'main.py': src})
        self.assertEqual(kind(fs, 'route'), [])
        notices = [n for n in fs['limitations'] if n['code'] == 'ROUTE_NOT_DECORATOR']
        self.assertEqual(len(notices), 2)
        self.assertTrue(any('main.py:3' in n['message'] for n in notices))
        self.assertTrue(any('main.py:4' in n['message'] for n in notices))

    def test_client_scopes_do_not_turn_database_get_into_http(self):
        src = '''import httpx
import aiohttp
async def a():
    async with httpx.AsyncClient() as session:
        await session.get("https://a.x/y?q=1")
async def b():
    session = aiohttp.ClientSession()
    await session.post("https://b.x/")
def database(session):
    session.get(Item, 1)
class Service:
    def __init__(self):
        self.client = httpx.AsyncClient()
    async def run(self):
        await self.client.request("GET", url)
'''
        calls = kind(facts_of({'main.py': src}), 'http_call')
        self.assertEqual(len(calls), 3)
        self.assertEqual(sorted(val(c, 'library') for c in calls), ['aiohttp', 'httpx', 'httpx'])
        self.assertIn('https://a.x/y', [val(c, 'url') for c in calls])
        self.assertEqual(sorted(val(c, 'method') for c in calls), ['GET', 'GET', 'POST'])

    def test_module_typed_client_and_shadowing(self):
        src = '''import httpx
client = httpx.Client()
def a():
    client.get("https://a.x")
def b(client):
    client.get(Item, 1)
def c(other: httpx.Client):
    other.get("https://c.x")
def d():
    client = database()
    client.get(Item, 1)
'''
        self.assertEqual(len(kind(facts_of({'main.py': src}), 'http_call')), 2)

    def test_config_key_and_unsupported_library(self):
        src = '''import requests
import urllib.request
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    PAYMENT_URL: str
settings = Settings()
requests.get(settings.PAYMENT_URL)
'''
        fs = facts_of({'main.py': src, 'tests/test_http.py': 'import requests\nrequests.get("https://test.x")\n'})
        [call] = kind(fs, 'http_call')
        self.assertEqual(val(call, 'url'), 'unknown')
        self.assertEqual(val(call, 'url_config_key'), 'PAYMENT_URL')
        self.assertEqual(val(call, 'library'), 'requests')
        self.assertTrue(any(n['code'] == 'HTTP_LIBRARY_UNSUPPORTED' for n in fs['limitations']))

    def test_http_readme_escaping_and_secret_redaction(self):
        src = 'import requests\nrequests.get("https://a.x/a|b")\nrequests.get("https://u:privatepass@a.x")\n'
        t, out, bundle = run_on({'main.py': src}, [('API', ['main.py'])])
        self.addCleanup(t.cleanup)
        text = (out / 'README.md').read_text(encoding='utf-8')
        self.assertIn('## Lời gọi HTTP ra ngoài', text)
        self.assertIn('a\\|b', text)
        self.assertIn('main.py:2', text)
        self.assertNotIn('privatepass', text)
        self.assertNotIn('privatepass', (out / 'result.json').read_text(encoding='utf-8'))

    def test_array_response_decorator_and_annotation(self):
        for annotation in ('list[UserOut]', 'List[UserOut]', 'Sequence[UserOut]', 'set[UserOut]'):
            for use_return in (False, True):
                with self.subTest(annotation=annotation, use_return=use_return):
                    src = ('from fastapi import FastAPI\nfrom pydantic import BaseModel\n'
                           'from typing import List, Sequence\nclass UserOut(BaseModel):\n    name: str\napp=FastAPI()\n')
                    src += (f'@app.get("/users")\ndef users() -> {annotation}: return []\n' if use_return else
                            f'@app.get("/users", response_model={annotation})\ndef users(): return []\n')
                    t, out, bundle = run_on({'main.py': src}, [('Users', ['main.py'])])
                    self.addCleanup(t.cleanup)
                    [api] = out.glob('tech-specs/*/api/*.md')
                    text = api.read_text(encoding='utf-8')
                    self.assertIn('list[UserOut]', text)
                    doc = json.loads(block(text, 'json'))
                    validate_openapi(doc)
                    schema = doc['paths']['/users']['get']['responses']['200']['content']['application/json']['schema']
                    self.assertEqual(schema['type'], 'array')
                    self.assertIn('$ref', schema['items'])

    def test_http_excerpts_do_not_expose_headers_or_password_arguments(self):
        fs = facts_of({'main.py': 'import requests\nrequests.get("https://a.x", headers={"Authorization": "Bearer TOPSECRET"})\n'
                       'requests.post("https://b.x", password="PASSWORDVALUE")\n'})
        self.assertEqual(len(kind(fs, 'http_call')), 2)
        self.assertNotIn('TOPSECRET', json.dumps(fs))
        self.assertNotIn('PASSWORDVALUE', json.dumps(fs))

    def test_client_rebinding_and_non_client_with_are_not_guessed(self):
        src = '''import httpx
client = httpx.Client()
def a():
    client = httpx.Client()
    client = database()
    client.get(Item, 1)
def b():
    with database() as client:
        client.get(Item, 1)
def c():
    if flag:
        other = httpx.Client()
    other.get(Item, 1)
'''
        self.assertEqual(kind(facts_of({'main.py': src}), 'http_call'), [])

    def test_request_keyword_method_and_environment_key(self):
        src = 'import aiohttp\nimport os\naiohttp.request(method="POST", url=os.environ["API_URL"])\n'
        [call] = kind(facts_of({'main.py': src}), 'http_call')
        self.assertEqual(val(call, 'method'), 'POST')
        self.assertEqual(val(call, 'url_config_key'), 'API_URL')

    def test_module_import_shadowed_by_parameter_is_not_http(self):
        fs = facts_of({'main.py': 'import requests\ndef query(requests):\n    requests.get(Item, 1)\n'})
        self.assertEqual(kind(fs, 'http_call'), [])
