"""Đợt 6: model gateway (CMP-006, API-006 §6) with fake providers and a fake clock. No real network."""
from __future__ import annotations

import json
import sys
import threading
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import contracts  # noqa: E402
from l3slice import extract, gateway, model, snapshot  # noqa: E402

FIX = HERE / "fixtures"
SENTINEL = "sk-SENTINELsecretvalue1234567890"
KEY = "gsk_" + "K" * 40


class Clock:
    def __init__(self):
        self.now = 0.0
        self.slept = []

    def __call__(self):
        return self.now

    def sleep(self, s):
        self.slept.append(s)
        self.now += s


def pipeline():
    snap, sources = snapshot.take(FIX / "shop_full")
    inv = snapshot.inventory(snap)
    unit = inv["units"][0]["id"]
    facts = extract.extract(snap, sources, unit)
    arch = model.build(snap, unit, facts, json.loads((FIX / "shop_full.membership.json").read_text(encoding="utf-8")))
    return snap, sources, inv, facts, arch


def context(snap, sources, replies=(), google=(), **over):
    clock = Clock()
    ctx = gateway.RunContext(
        run_id="run_g", snapshot_id=snap["snapshot_id"], sources=sources,
        files={f["file_id"]: f for f in snap["files"]},
        disclosure={"snapshot_id": snap["snapshot_id"], "notice_version": "l3gen-egress-v1", "providers": ["groq", "google"]},
        keys={"groq": gateway.KeyHandle(KEY), "google": gateway.KeyHandle("AIza" + "G" * 35)},
        providers={"groq": gateway.FakeProvider(replies), "google": gateway.FakeProvider(google)},
        capabilities={(p, m, k): True for k, (p, m) in gateway.ROUTES.items()},
        free_only={"groq": True, "google": True}, ledger=gateway.Ledger(clock, clock.sleep))
    for k, v in over.items():
        setattr(ctx, k, v)
    return ctx


def label_request(snap, facts, arch, request_id="req_label", max_out=800):
    comp = arch["components"][0]
    members = set(comp["member_file_ids"])
    facts = dict(facts, facts=[f for f in facts["facts"] if f["evidence"] and f["evidence"][0]["file_id"] in members])
    req = {"schema_version": "0.1.0", "run_id": "run_g", "request_id": request_id, "snapshot_id": snap["snapshot_id"],
           "kind": "label_components", "scope_id": f"component:{comp['id']}", "file_ids": comp["member_file_ids"],
           "fact_set": facts, "components": [comp], "edges": [], "prompt_version": gateway.PROMPT_VERSION,
           "tool_version": gateway.TOOL_VERSION, "max_output_tokens": max_out}
    contracts.validate(req, 6, "ModelRequest")
    return req


def edges_request(snap, facts, arch, request_id="req_edges"):
    req = {"schema_version": "0.1.0", "run_id": "run_g", "request_id": request_id, "snapshot_id": snap["snapshot_id"],
           "kind": "propose_edges", "scope_id": f"repository:{snap['snapshot_id']}",
           "file_ids": [f["file_id"] for f in snap["files"]], "fact_set": facts, "components": arch["components"],
           "edges": arch["edges"], "prompt_version": gateway.PROMPT_VERSION, "tool_version": gateway.TOOL_VERSION,
           "max_output_tokens": 2000}
    contracts.validate(req, 6, "ModelRequest")
    return req


def groq(content=None, tool_calls=None, usage=True):
    body = {"choices": [{"message": {"content": content, "tool_calls": tool_calls}}]}
    if usage:
        body["usage"] = {"prompt_tokens": 500, "completion_tokens": 100}
    return body


def gemini(result):
    return {"candidates": [{"content": {"parts": [{"text": json.dumps(result)}]}}],
            "usageMetadata": {"promptTokenCount": 900, "candidatesTokenCount": 50}}


def label_result(arch, facts, **extra):
    comp = arch["components"][0]
    item = {"component_id": comp["id"], "name": "Kho", "description": "Lưu bảng", "role": "lưu trữ",
            "fact_ids": [facts["facts"][0]["id"]], **extra}
    return {"kind": "label_components", "component_labels": [item], "edge_labels": []}


class Gateway(unittest.TestCase):
    def setUp(self):
        self.snap, self.sources, self.inv, self.facts, self.arch = pipeline()
        self.ok_reply = json.dumps(label_result(self.arch, self.facts))

    def ctx(self, replies=(), google=(), **over):
        return context(self.snap, self.sources, replies, google, **over)

    def resp(self, r):
        contracts.validate(r, 6, "ModelResponse")
        return r

    def test_label_two_phases_ok(self):
        ctx = self.ctx([groq(""), groq(self.ok_reply)])
        r = self.resp(gateway.invoke_model(label_request(self.snap, self.facts, self.arch), ctx))
        self.assertEqual(r["status"], "ok")
        sent = ctx.providers["groq"].sent
        self.assertEqual(len(sent), 2)
        self.assertIn("tools", sent[0])
        self.assertNotIn("tools", sent[1])
        self.assertEqual(sent[1]["response_format"], {"type": "json_object"})
        self.assertEqual([p["usage_source"] for p in r["provenance"]], ["provider", "provider"])

    def test_preflight_errors_send_nothing(self):
        cases = {"DISCLOSURE_REQUIRED": {"disclosure": None},
                 "MISSING_KEY": {"keys": {}},
                 "PAID_ROUTE_DISABLED": {"free_only": {}},
                 "CAPABILITY_UNVERIFIED": {"capabilities": {}}}
        for code, over in cases.items():
            ctx = self.ctx([groq(self.ok_reply)], **over)
            r = self.resp(gateway.invoke_model(label_request(self.snap, self.facts, self.arch), ctx))
            self.assertEqual(r["error"]["code"], code)
            self.assertEqual(ctx.providers["groq"].sent, [])
        stale = dict(self.ctx().disclosure, notice_version="old")
        r = gateway.invoke_model(label_request(self.snap, self.facts, self.arch), self.ctx(disclosure=stale))
        self.assertEqual(r["error"]["code"], "DISCLOSURE_REQUIRED")

    def test_extra_membership_key_is_schema_invalid(self):
        bad = json.dumps(label_result(self.arch, self.facts, member_file_ids=["file:x"]))
        r = self.resp(gateway.invoke_model(label_request(self.snap, self.facts, self.arch), self.ctx([groq(""), groq(bad)])))
        self.assertEqual((r["status"], r["error"]["code"], r["result"]), ("error", "SCHEMA_INVALID", None))

    def test_unknown_ids_are_dropped(self):
        res = label_result(self.arch, self.facts)
        res["component_labels"].append(dict(res["component_labels"][0], component_id="cmp_unknown"))
        res["component_labels"].append(dict(res["component_labels"][0], fact_ids=["fact:unknown"]))
        res["component_labels"].append(dict(res["component_labels"][0], name="trùng"))
        ctx = self.ctx([groq(""), groq(json.dumps(res))])
        r = self.resp(gateway.invoke_model(label_request(self.snap, self.facts, self.arch), ctx))
        self.assertEqual([x["name"] for x in r["result"]["component_labels"]], ["Kho"])
        self.assertIn({"event": "items_dropped", "request_id": "req_label", "key": "component_labels", "count": 3}, ctx.log)

    def test_group_retry_uses_both_gemini_slots(self):
        unit = self.inv["units"][0]
        flat = {"unit_id": unit["id"], "flat": True, "file_ids": unit["file_ids"]}
        group = {"schema_version": "0.1.0", "run_id": "run_g", "request_id": "req_group", "snapshot_id": self.snap["snapshot_id"],
                 "kind": "group_flat", "scope_id": f"repository:{self.snap['snapshot_id']}", "file_ids": flat["file_ids"],
                 "fact_set": self.facts, "components": [], "edges": [], "flat_units": [flat],
                 "prompt_version": gateway.PROMPT_VERSION, "tool_version": gateway.TOOL_VERSION, "max_output_tokens": 2000}
        contracts.validate(group, 6, "ModelRequest")
        result = {"kind": "group_flat", "groups": [{"proposal_id": "g1", "unit_id": flat["unit_id"], "file_ids": flat["file_ids"], "reason": "x"}]}
        ctx = self.ctx(google=[gateway.Transient, gemini(result)])
        r = self.resp(gateway.invoke_model(group, ctx))
        self.assertEqual(r["status"], "ok")
        self.assertEqual(len(ctx.providers["google"].sent), 2)
        self.assertEqual([p["usage_source"] for p in r["provenance"]], ["reserved_upper_bound", "provider"])
        self.assertEqual(ctx.ledger.sleep.__self__.slept[:1], [1])
        r2 = self.resp(gateway.invoke_model(edges_request(self.snap, self.facts, self.arch), ctx))
        self.assertEqual((r2["error"]["code"], r2["error"]["scope"]), ("RUN_BUDGET_EXHAUSTED", "run"))
        self.assertEqual(len(ctx.providers["google"].sent), 2)

    def test_send_40_admitted_41_blocked(self):
        ctx = self.ctx([groq("", tool_calls=[{"id": "c1", "function": {"name": "read_code", "arguments": "{}"}}]),
                        groq(self.ok_reply)])
        ctx.ledger._run("run_g")["physical"] = 39
        r = self.resp(gateway.invoke_model(label_request(self.snap, self.facts, self.arch), ctx))
        self.assertEqual(len(ctx.providers["groq"].sent), 1)
        self.assertEqual((r["status"], r["error"]["code"], r["result"]), ("error", "RUN_BUDGET_EXHAUSTED", None))
        self.assertEqual(ctx.ledger.runs["run_g"]["physical"], 40)

    def test_request_over_6000_tokens_sends_nothing(self):
        with self.assertRaises(gateway.GatewayError) as e:
            gateway.Ledger().reserve("r", "groq", "fp", 5500 + 1000)
        self.assertEqual(e.exception.code, "INPUT_TOO_LARGE")
        ctx = self.ctx([groq(self.ok_reply)])
        r = self.resp(gateway.invoke_model(label_request(self.snap, self.facts, self.arch, max_out=6000), ctx))
        self.assertEqual(r["error"]["code"], "INPUT_TOO_LARGE")
        self.assertEqual(ctx.providers["groq"].sent, [])

    def test_429_is_not_retried(self):
        ctx = self.ctx([{"_http_status": 429}, groq(self.ok_reply)])
        r = self.resp(gateway.invoke_model(label_request(self.snap, self.facts, self.arch), ctx))
        self.assertEqual(r["error"]["code"], "RATE_LIMITED")
        self.assertEqual(len(ctx.providers["groq"].sent), 1)

    def test_three_timeouts_stop_the_task(self):
        ctx = self.ctx([gateway.Transient] * 4)
        r = self.resp(gateway.invoke_model(label_request(self.snap, self.facts, self.arch), ctx))
        self.assertEqual(r["error"]["code"], "TIMEOUT")
        self.assertEqual(len(ctx.providers["groq"].sent), 3)
        self.assertEqual(ctx.ledger.sleep.__self__.slept, [1, 2])
        self.assertTrue(all(p["usage_source"] == "reserved_upper_bound" for p in r["provenance"]))

    def test_secret_and_key_never_leave(self):
        arch = json.loads(json.dumps(self.arch))
        arch["components"][0]["name"] = f'password = "{SENTINEL}"'
        ctx = self.ctx([groq(""), groq(self.ok_reply)])
        r = gateway.invoke_model(label_request(self.snap, self.facts, arch), ctx)
        dumped = json.dumps([ctx.providers["groq"].sent, ctx.log, r]) + repr(ctx.keys)
        self.assertNotIn(SENTINEL, dumped)
        self.assertNotIn(KEY, dumped)
        json.loads(ctx.providers["groq"].sent[0]["messages"][1]["content"])  # masking keeps JSON valid

    def test_mask_reaches_nested_lists(self):
        out = gateway.mask_obj({"a": [{"b": [f"token = '{SENTINEL}'", SENTINEL]}]})
        self.assertNotIn(SENTINEL, json.dumps(out))

    def test_cache_by_request_id(self):
        ctx = self.ctx([groq(""), groq(self.ok_reply)])
        req = label_request(self.snap, self.facts, self.arch)
        first = gateway.invoke_model(req, ctx)
        self.assertIs(gateway.invoke_model(req, ctx), first)
        self.assertEqual(len(ctx.providers["groq"].sent), 2)
        other = dict(req, max_output_tokens=900)
        self.assertEqual(gateway.invoke_model(other, ctx)["error"]["code"], "INVALID_INPUT")

    def test_shared_credential_threads_do_not_overrun(self):
        ledger = gateway.Ledger(clock=lambda: 0.0, sleep=lambda s: (_ for _ in ()).throw(TimeoutError()))
        ok, refused = [], []

        def worker():
            for _ in range(10):
                try:
                    ledger.reserve("run_a", "groq", "fp", 100)
                    ok.append(1)
                except (gateway.GatewayError, TimeoutError):
                    refused.append(1)
        threads = [threading.Thread(target=worker) for _ in range(5)]
        [t.start() for t in threads]
        [t.join() for t in threads]
        self.assertEqual(len(ok), 30)  # Groq 30 requests/minute, fake clock never advances
        self.assertEqual(ledger.runs["run_a"]["physical"], 30)


class ReadCode(unittest.TestCase):
    def setUp(self):
        self.snap, self.sources, _, self.facts, self.arch = pipeline()
        self.ctx = context(self.snap, self.sources)
        self.comp = self.arch["components"][0]
        self.file_id = self.comp["member_file_ids"][0]
        self.lines = len(self.sources[self.ctx.files[self.file_id]["path"]].decode().splitlines())

    def read(self, **kw):
        req = {"request_id": "r", "snapshot_id": self.snap["snapshot_id"], "scope_id": f"component:{self.comp['id']}",
               "file_id": self.file_id, "start_line": 1, "line_count": 2, **kw}
        out = gateway.read_code(req, self.ctx, set(self.comp["member_file_ids"]), "groq", "label_components")
        contracts.validate(out, 6, "CodeReadResult")
        return out

    def test_denials_count_toward_quota(self):
        other = next(f["file_id"] for f in self.snap["files"] if f["file_id"] != self.file_id)
        self.assertEqual(self.read(file_id=other)["error_code"], "OUTSIDE_SCOPE")
        self.assertEqual(self.read(snapshot_id="snap:other")["error_code"], "WRONG_SNAPSHOT")
        self.assertEqual(self.read(start_line=self.lines, line_count=2)["error_code"], "INVALID_RANGE")
        ok = self.read()
        self.assertEqual(ok["status"], "ok")
        self.assertEqual(ok["evidence"]["start_line"], 1)
        self.read(start_line=3, line_count=1)
        self.read(start_line=4, line_count=1)
        self.assertEqual(self.read(start_line=5, line_count=1)["error_code"], "READ_LIMIT")

    def test_union_cannot_cover_whole_file(self):
        self.assertEqual(self.read(start_line=1, line_count=self.lines - 1)["status"], "ok")
        self.assertEqual(self.read(start_line=self.lines, line_count=1)["error_code"], "WHOLE_FILE_DISCLOSURE")

    def test_only_label_task_has_the_tool(self):
        req = {"request_id": "r", "snapshot_id": self.snap["snapshot_id"], "scope_id": "s", "file_id": self.file_id,
               "start_line": 1, "line_count": 1}
        self.assertEqual(gateway.read_code(req, self.ctx, {self.file_id}, "google", "propose_edges")["error_code"], "WRONG_TASK")


if __name__ == "__main__":
    unittest.main()
