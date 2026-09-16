"""Các ca khóa hành vi cho Resolver + Dataflow V2."""

import ast

from l3gen.core.resolution.dataflow import resolve_program
from l3gen.languages.python.frontend import build_semantic_program
from l3gen.languages.python.parser import ParsedFile


def resolve(source: str):
    parsed = ParsedFile("main.py", ast.parse(source), source.count("\n") + 1)
    program = build_semantic_program([parsed], {"main.py": "main"})
    return resolve_program(program)


def call(result, written_callee: str):
    matches = [item for item in result.calls if item.written_callee == written_callee]
    assert matches, f"không có call {written_callee!r}"
    return matches[-1]


def test_alias_factory_va_framework_method_duoc_resolve_qua_dataflow():
    result = resolve(
        """
from fastapi import FastAPI as Application
factory = Application
app = factory()
child = Application()
app.mount("/child", app=child)
"""
    )

    assert call(result, "factory").targets == ["fastapi.FastAPI"]
    mounted = call(result, "app.mount")
    assert mounted.status == "resolved"
    assert mounted.targets == ["starlette.applications.Starlette.mount"]
    assert mounted.receiver_types == ["fastapi.FastAPI"]
    assert mounted.receiver_slot
    assert mounted.keyword_slots["app"]


def test_argument_return_va_method_noi_duoc_xuyen_qua_ham_noi_bo():
    result = resolve(
        """
class Handler:
    def run(self):
        return 1

def identity(value):
    return value

handler = identity(Handler())
handler.run()
"""
    )

    resolved = call(result, "handler.run")
    assert resolved.status == "resolved"
    assert resolved.targets == ["main.Handler.run"]
    assert resolved.receiver_types == ["main.Handler"]


def test_nhanh_dieu_kien_giu_tap_candidates_thay_vi_doan_bua_mot_dich():
    result = resolve(
        """
class A:
    def run(self): pass
class B:
    def run(self): pass
handler = A() if flag else B()
handler.run()
"""
    )

    resolved = call(result, "handler.run")
    assert resolved.status == "candidates"
    assert resolved.targets == ["main.A.run", "main.B.run"]


def test_getattr_dong_duoc_ghi_runtime_ro_rang():
    result = resolve(
        """
import handlers
handler_name = config["handler"]
handler_class = getattr(handlers, handler_name)
handler = handler_class()
handler.run()
"""
    )

    assert call(result, "getattr").status == "resolved"
    assert call(result, "handler_class").status == "runtime"
    assert call(result, "handler.run").status == "runtime"


def test_shadowing_chon_binding_moi_nhat_co_hieu_luc_tai_call_site():
    result = resolve(
        """
from fastapi import FastAPI
def FastAPI():
    return 1
app = FastAPI()
"""
    )

    resolved = call(result, "FastAPI")
    assert resolved.status == "resolved"
    assert resolved.targets == ["main.FastAPI"]


def test_hai_router_cung_type_van_co_danh_tinh_object_khac_nhau():
    result = resolve(
        """
from fastapi import APIRouter
first = APIRouter()
second = APIRouter()
"""
    )

    allocations = {
        value.value
        for values in result.values_by_slot.values()
        for value in values
        if value.kind == "instance" and value.type_symbol == "fastapi.APIRouter"
    }
    assert len(allocations) == 2


def test_constructor_truyen_argument_vao_self_attribute_roi_doc_lai_o_method():
    result = resolve(
        """
class Client:
    def send(self): pass
class Service:
    def __init__(self, client):
        self.client = client
    def run(self):
        self.client.send()
service = Service(Client())
service.run()
"""
    )

    resolved = call(result, "self.client.send")
    assert resolved.status == "resolved"
    assert resolved.targets == ["main.Client.send"]
