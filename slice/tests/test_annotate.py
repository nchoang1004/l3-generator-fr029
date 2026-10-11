"""Đợt 7: model tasks in CMP-005 through the gateway (fake providers). Proposals must be proven by static rules."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import contracts  # noqa: E402
from l3slice import annotate, gateway, render, verify  # noqa: E402
from test_gateway import context, gemini, groq, pipeline  # noqa: E402


def facts_of(facts, comp):
    return [f["id"] for f in facts["facts"] if f["evidence"] and f["evidence"][0]["file_id"] in comp["member_file_ids"]]


class Annotate(unittest.TestCase):
    def setUp(self):
        self.snap, self.sources, self.inv, self.facts, self.arch = pipeline()
        self.by_name = {c["name"]: c for c in self.arch["components"]}
        self.api, self.store = self.by_name["Cửa hàng API"], self.by_name["Lưu trữ"]

    def label(self, comp, name, fact_ids=None):
        return groq(json.dumps({"kind": "label_components", "component_labels": [
            {"component_id": comp["id"], "name": name, "description": "mô tả", "role": "vai trò",
             "fact_ids": fact_ids or facts_of(self.facts, comp)[:1]}], "edge_labels": []}))

    def run_all(self, labels, proposals):
        replies = []
        for comp, reply in zip(self.arch["components"], labels):
            replies += [groq(""), reply]
        ctx = context(self.snap, self.sources, replies, [gemini({"kind": "propose_edges", "proposals": proposals})])
        out = annotate.annotate(self.arch, self.facts, self.snap, ctx)
        contracts.validate(out, 5, "ArchitectureModel")
        return out, ctx

    def test_labels_and_proven_proposal(self):
        static = self.arch["edges"][0]
        ref = static["fact_ids"][0]
        target = next(f for f in self.facts["facts"] if f["id"] == ref)["target_fact_ids"][0]
        sym_api = next(i for i in facts_of(self.facts, self.api) if i != ref)
        sym_store = next(i for i in facts_of(self.facts, self.store) if i != target)
        proposals = [
            {"proposal_id": "p_ok", "source_component_id": self.api["id"], "target_component_id": self.store["id"],
             "relation_type": "calls", "fact_ids": [ref, target], "reason": "gọi hàm lưu"},
            {"proposal_id": "p_unproven", "source_component_id": self.api["id"], "target_component_id": self.store["id"],
             "relation_type": "depends_on", "fact_ids": [sym_api, sym_store], "reason": "tên giống"},
            {"proposal_id": "p_one_end", "source_component_id": self.store["id"], "target_component_id": self.api["id"],
             "relation_type": "calls", "fact_ids": [target, sym_store], "reason": "đoán"}]
        labels = [self.label(c, f"Nhãn {c['name']}") for c in self.arch["components"]]
        out, ctx = self.run_all(labels, proposals)
        self.assertEqual({c["label_status"] for c in out["components"]}, {"model_labeled"})
        self.assertEqual(len(out["edges"]), 1)
        self.assertEqual((out["edges"][0]["origin"], out["edges"][0]["confidence"]), ("static", "exact"))
        self.assertEqual(len(out["edges"][0]["provenance"]), 1)
        self.assertEqual({(r["proposal_id"], r["reason_code"]) for r in out["rejected_proposals"]},
                         {("p_unproven", "UNPROVEN_BINDING"), ("p_one_end", "MISSING_ENDPOINT_EVIDENCE")})
        self.assertNotIn(annotate.NOT_RUN, [lim["code"] for lim in out["limitations"]])
        self.assertEqual(ctx.ledger.runs["run_g"]["physical"], 5)
        verified = verify.verify(self.snap, self.sources, self.inv, self.facts, out)
        with tempfile.TemporaryDirectory() as t:
            bundle = render.render(verified, "run_a", "shop_full", Path(t) / "out")
            readme = (Path(t) / "out/README.md").read_text(encoding="utf-8")
        contracts.check_bundle_invariants(bundle)
        self.assertIn("Nhãn Cửa hàng API", readme)

    def test_label_with_foreign_fact_is_rejected(self):
        ref = self.arch["edges"][0]["fact_ids"][0]
        target = next(f for f in self.facts["facts"] if f["id"] == ref)["target_fact_ids"]  # in the request, not in API files
        bad = self.label(self.api, "Sai", target)
        labels = [bad if c["id"] == self.api["id"] else self.label(c, "Kho") for c in self.arch["components"]]
        out, _ = self.run_all(labels, [])
        api = next(c for c in out["components"] if c["id"] == self.api["id"])
        self.assertEqual((api["name"], api["label_status"]), ("Cửa hàng API", "path_fallback"))
        self.assertEqual([r["reason_code"] for r in out["rejected_proposals"]], ["OUTSIDE_SCOPE"])

    def test_gateway_failure_keeps_static_model(self):
        ctx = context(self.snap, self.sources, keys={})
        out = annotate.annotate(self.arch, self.facts, self.snap, ctx)
        contracts.validate(out, 5, "ArchitectureModel")
        self.assertEqual(out["edges"], self.arch["edges"])
        self.assertEqual([c["name"] for c in out["components"]], [c["name"] for c in self.arch["components"]])
        self.assertEqual({lim["code"] for lim in out["limitations"]}, {"MISSING_KEY"})
        self.assertEqual(ctx.providers["groq"].sent + ctx.providers["google"].sent, [])


class CliLlm(unittest.TestCase):
    def test_keys_from_prompt_never_reach_output(self):
        from unittest import mock
        from l3slice import __main__ as cli
        key = "gsk_" + "Z" * 40
        fix = HERE / "fixtures"
        with tempfile.TemporaryDirectory() as t, mock.patch.object(cli.getpass, "getpass", return_value=key):
            out = Path(t) / "out"
            code = cli.main(["--source", str(fix / "shop_full"), "--output", str(out),
                             "--membership", str(fix / "shop_full.membership.json"), "--llm"])
            texts = [p.read_bytes() for p in out.rglob("*") if p.is_file()]
            result = json.loads((out / "result.json").read_text(encoding="utf-8"))
        self.assertEqual(code, 3)
        self.assertFalse(any(key.encode() in b for b in texts))
        codes = {lim["code"] for lim in result["result"]["limitations"]}
        self.assertIn("PAID_ROUTE_DISABLED", codes)  # free-only route not verified: nothing is sent
        self.assertNotIn("MODEL_NOT_RUN", codes)


class FlatGroups(unittest.TestCase):
    def setUp(self):
        self.base = {"snapshot_id": "s1", "limitations": [], "rejected_proposals": []}
        self.units = {"u1": ["f_a", "f_b", "f_c"]}

    def resp(self, groups):
        return {"schema_version": "0.1.0", "request_id": "group:s1", "snapshot_id": "s1", "kind": "group_flat",
                "status": "ok", "result": {"kind": "group_flat", "groups": groups}, "error": None,
                "provenance": [{"request_id": "group:s1", "provider": "google", "model": "gemini-3.5-flash",
                                "prompt_version": "p", "tool_version": "t", "snapshot_id": "s1", "physical_requests": 1,
                                "input_tokens": 1, "output_tokens": 1, "usage_source": "provider"}]}

    def test_valid_partition(self):
        comps = annotate.apply_groups(self.base, self.units, self.resp(
            [{"proposal_id": "g1", "unit_id": "u1", "file_ids": ["f_a", "f_b"], "reason": "x"},
             {"proposal_id": "g2", "unit_id": "u1", "file_ids": ["f_c"], "reason": "y"}]), "policy-x")
        self.assertEqual(sorted(len(c["member_file_ids"]) for c in comps), [1, 2])
        self.assertEqual({c["grouping_source"] for c in comps}, {"llm"})
        for c in comps:
            contracts.validate(c, 5, "Component")

    def test_duplicate_file_falls_back_to_one_component(self):
        comps = annotate.apply_groups(self.base, self.units, self.resp(
            [{"proposal_id": "g1", "unit_id": "u1", "file_ids": ["f_a", "f_b"], "reason": "x"},
             {"proposal_id": "g2", "unit_id": "u1", "file_ids": ["f_a"], "reason": "y"}]), "policy-x")
        self.assertEqual([c["member_file_ids"] for c in comps], [["f_a", "f_b", "f_c"]])
        self.assertEqual(comps[0]["grouping_source"], "fallback")
        contracts.validate(comps[0], 5, "Component")
        self.assertEqual(self.base["rejected_proposals"][0]["reason_code"], "MEMBERSHIP_MISMATCH")


if __name__ == "__main__":
    unittest.main()
