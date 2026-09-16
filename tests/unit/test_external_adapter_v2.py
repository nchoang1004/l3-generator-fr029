import ast

from l3gen.core.resolution.dataflow import resolve_program
from l3gen.languages.python.frameworks.fastapi.external_v2 import extract_external_calls_v2
from l3gen.languages.python.frontend import build_semantic_program
from l3gen.languages.python.parser import ParsedFile


def external(source: str):
    parsed = ParsedFile("main.py", ast.parse(source), source.count("\n") + 1)
    program = build_semantic_program([parsed], {"main.py": "main"})
    return extract_external_calls_v2(program, resolve_program(program))


def test_alias_client_request_va_try_duoc_nhan_bang_symbol():
    result = external(
        """
import httpx as transport
def pay():
    client = transport.Client()
    try:
        return client.post("https://payment.internal/charge")
    except Exception:
        return None
"""
    )
    assert len(result) == 1
    assert result[0].http_method == "POST"
    assert result[0].url_or_host == "https://payment.internal/charge"
    assert result[0].inside_try_except is True


def test_method_trung_ten_cua_class_noi_bo_khong_bi_nhan_nham_http():
    result = external(
        """
class Store:
    def get(self, key): pass
def read():
    store = Store()
    return store.get("orders")
"""
    )
    assert result == []

