"""Invariants of the FR-029 scoring tools, on synthetic data only (review 07/10/2026: scorer + golden audit).

Each test pins one confirmed fault: alias vs exact, duplicate facts, kinds without gold, unknown counted as
correct, array rank, golden-v1 adapter (HTTP span, non-HTTP libraries, `{prefix}` placeholder, scored scope)
and the consensus key of the grade merge.
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE.parent / "tools")]

import fr029_accept  # noqa: E402
import fr029_golden4  # noqa: E402
import fr029_golden_routes  # noqa: E402
import fr029_grade_merge  # noqa: E402
import fr029_score  # noqa: E402


def known(v):
    return {"state": "known", "value": v}


def http_fact(fid, method, line=1, url="https://x"):
    return {"id": fid, "kind": "http_call", "confidence": "exact",
            "evidence": [{"path": "a.py", "start_line": line}],
            "attributes": {"library": known("httpx"), "method": known(method),
                           "url": known(url) if url else {"state": "unknown"}}}


def result_of(*facts):
    return {"facts": list(facts), "components": [], "limitations": []}


HTTP_GOLD = {"routes": [], "models": [], "limitations": [],
             "http_calls": [{"where": "a.py:1", "library": "httpx", "method": "GET",
                             "target": {"kind": "literal", "value": "https://x"}}]}


class ExactUsesTheSameMatching(unittest.TestCase):
    def test_alias_location_keeps_the_wrong_method(self):
        gold = {"routes": [], "models": [], "limitations": [],
                "http_calls": [{"where": "a.py:2", "alt_where": ["a.py:3"], "library": "httpx", "method": "GET",
                                "target": {"kind": "literal", "value": "https://x"}}]}
        result = result_of(http_fact("f1", "POST", line=3))
        rep = fr029_score.score(result, gold)
        self.assertEqual(rep["http_calls"]["tp"], 1)
        self.assertEqual(len(rep["http_calls"]["attributes"]["method"]["wrong"]), 1)
        ex = fr029_accept.exact_wrong(result, rep)
        self.assertEqual((ex["exact_facts"], ex["exact_wrong"]), (1, 1))

    def test_duplicates_score_the_same_in_any_order(self):
        seen = []
        for order in (("POST", "GET"), ("GET", "POST")):
            result = result_of(*(http_fact(f"f-{m}", m) for m in order))
            rep = fr029_score.score(result, HTTP_GOLD)
            ex = fr029_accept.exact_wrong(result, rep)
            seen.append((rep["http_calls"]["tp"], rep["http_calls"]["fp"],
                         rep["http_calls"]["attributes"]["method"]["correct"], ex["exact_facts"], ex["exact_wrong"]))
        self.assertEqual(seen[0], seen[1])
        self.assertEqual(seen[0], (1, 1, 1, 2, 1))  # the GET fact matches; the extra POST is a wrong extra fact

    def test_http_evidence_range_holding_the_call_line_matches(self):
        gold = {"routes": [], "models": [], "limitations": [],
                "http_calls": [{"where": "a.py:84", "library": "httpx", "method": "GET",
                                "target": {"kind": "literal", "value": "https://x"}}]}
        fact = dict(http_fact("f1", "GET"), evidence=[{"path": "a.py", "start_line": 83, "end_line": 84}])
        rep = fr029_score.score(result_of(fact), gold)
        self.assertEqual((rep["http_calls"]["tp"], rep["http_calls"]["fp"], rep["http_calls"]["fn"]), (1, 0, 0))

    def test_route_response_accepts_the_model_alt_names(self):
        model = {"id": "m1", "kind": "model", "confidence": "exact", "evidence": [{"path": "t.py", "start_line": 1}],
                 "attributes": {"name": known("TextSummary"), "declared_in": known("t.py"), "fields": known([])}}
        route = {"id": "r1", "kind": "route", "confidence": "exact", "evidence": [{"path": "v.py", "start_line": 3}],
                 "attributes": {"method": known("GET"), "path": known("/s"), "handler": known("v.py::get"),
                                "parameters": known([]), "request_model_ids": known([]), "response_model_ids": known(["m1"]),
                                "bodies": known([{"direction": "response", "model_id": "m1", "array": False}]),
                                "status_codes": known([200])}}
        gold = {"routes": [{"method": "GET", "path": "/s", "declared_at": "v.py:3", "handler": "v.py::get", "params": [],
                            "request_body": None, "response": {"model": "SummarySchema", "model_file": "t.py", "array": False},
                            "status": [200]}],
                "models": [{"file": "t.py", "name": "SummarySchema", "alt_names": ["TextSummary"], "fields": []}],
                "limitations": []}
        rep = fr029_score.score(result_of(model, route), gold)
        self.assertEqual(len(rep["routes"]["attributes"]["response"]["wrong"]), 0)

    def test_extra_limitations_the_gold_accepts_are_not_false_positives(self):
        result = dict(result_of(), limitations=[{"code": "HTTP_LIBRARY_UNSUPPORTED", "where": "a.py:3",
                                                 "message": "unsupported_http_library openai"}])
        gold = {"routes": [], "models": [], "limitations": [],
                "accept_extra_limitations": [{"kind": "unsupported_http_library"}]}
        rep = fr029_score.score(result, gold)
        self.assertEqual((rep["limitations"]["fp"], rep["limitations"]["accepted_extra"]), (0, 1))

    def test_out_of_scope_zero_counts_equal_absent_keys(self):
        result = dict(result_of(), coverage={"not_readable": [{"scope": "test"}]})
        rep = fr029_score.score(result, {"routes": [], "models": [], "limitations": [],
                                         "out_of_scope": {"test": 1, "environment": 0}})
        self.assertTrue(rep["out_of_scope"]["ok"])

    def test_kind_without_gold_is_not_in_the_exact_denominator(self):
        result = result_of(http_fact("f1", "GET"))
        rep = fr029_score.score(result, {"routes": [], "models": [], "limitations": []})
        self.assertEqual(rep["http_calls"]["status"], "not_evaluated")
        ex = fr029_accept.exact_wrong(result, rep)
        self.assertEqual((ex["exact_facts"], ex["exact_wrong"], ex["rate"], ex["not_evaluated"]), (0, 0, None, 1))

    def test_missing_models_key_is_not_evaluated_instead_of_false_positives(self):
        model = {"id": "m1", "kind": "model", "confidence": "exact", "evidence": [{"path": "m.py", "start_line": 1}],
                 "attributes": {"name": known("A"), "declared_in": known("m.py"), "fields": known([])}}
        rep = fr029_score.score(result_of(model), {"routes": [], "limitations": []})
        self.assertEqual(rep["models"]["status"], "not_evaluated")


class UnknownIsNotCorrect(unittest.TestCase):
    def test_unknown_target_matching_unknown_gold_is_acceptable_not_correct(self):
        gold = {"routes": [], "models": [], "limitations": [],
                "http_calls": [{"where": "a.py:1", "library": "httpx", "method": "GET", "target": {"kind": "unknown"}}]}
        rep = fr029_score.score(result_of(http_fact("f1", "GET", url=None)), gold)
        t = rep["http_calls"]["attributes"]["target"]
        self.assertEqual((t["correct"], t["acceptable_unknown"], len(t["wrong"])), (0, 1, 0))

    def test_dynamic_model_without_fields_is_acceptable_unknown(self):
        want = {"unknown_ok": True, "fields": [("x", None, "string", True, False)], "alt_types": {}}
        self.assertEqual(fr029_score._fields_ok([], want), "unknown")
        self.assertEqual(fr029_score._fields_ok([("x", None, None, None, None)], want), "unknown")
        self.assertEqual(fr029_score._fields_ok([("x", None, "string", True, False)], want), "correct")
        self.assertEqual(fr029_score._fields_ok([("x", None, "integer", True, False)], want), "wrong")


class PathConverters(unittest.TestCase):
    def test_converter_in_a_path_is_the_same_endpoint(self):
        route = {"id": "r1", "kind": "route", "confidence": "exact", "evidence": [{"path": "m.py", "start_line": 3}],
                 "attributes": {"method": known("GET"), "path": known("/s/{p:path}"), "handler": known("m.py::f"),
                                "parameters": known([]), "request_model_ids": known([]), "response_model_ids": known([]),
                                "status_codes": known([200])}}
        gold = {"routes": [{"method": "GET", "path": "/s/{p}", "declared_at": "m.py:3", "handler": "m.py::f",
                            "params": [], "request_body": None, "response": None, "status": [200]}],
                "models": [], "limitations": []}
        rep = fr029_score.score(result_of(route), gold)
        self.assertEqual((rep["routes"]["tp"], rep["routes"]["fp"], rep["routes"]["fn"]), (1, 0, 0))


class HeaderNames(unittest.TestCase):
    def test_header_names_compare_without_case(self):
        route = {"id": "r1", "kind": "route", "confidence": "exact", "evidence": [{"path": "v.py", "start_line": 3}],
                 "attributes": {"method": known("GET"), "path": known("/u"), "handler": known("v.py::u"),
                                "parameters": known([{"name": known("authorization"), "in": known("header"),
                                                      "schema": known({"type": "string"}), "required": known(False)}]),
                                "request_model_ids": known([]), "response_model_ids": known([]), "status_codes": known([200])}}
        gold = {"routes": [{"method": "GET", "path": "/u", "declared_at": "v.py:3", "handler": "v.py::u",
                            "params": [{"name": "Authorization", "in": "header", "type": "string", "required": False}],
                            "request_body": None, "response": None, "status": [200]}], "models": [], "limitations": []}
        rep = fr029_score.score(result_of(route), gold)
        self.assertEqual(rep["routes"]["attributes"]["params"]["wrong"], [])


class ArrayRank(unittest.TestCase):
    def test_nested_arrays_keep_their_rank(self):
        self.assertNotEqual(fr029_score._type_response("array[array[integer]]", False),
                            fr029_score._type_response("array[integer]", False))
        self.assertEqual(fr029_score._type_response("array[integer]", False),
                         fr029_score._type_response("integer", True))


class TypeNotation(unittest.TestCase):
    def test_formats_follow_the_notation_of_the_gold(self):
        # notation 7.3 (same as docfacts.BASE_TYPES): uuid, date, datetime, email keep their name; uri/binary/time
        # have no name of their own and stay string
        cases = {"uuid": "uuid", "date": "date", "date-time": "datetime", "email": "email",
                 "binary": "string", "uri": "string", "time": "string"}
        for fmt, want in cases.items():
            with self.subTest(fmt):
                self.assertEqual(fr029_score.type_text({"type": "string", "format": fmt}, {}), want)
        self.assertEqual(fr029_score.type_text({"type": "array", "items": {"type": "string", "format": "uuid"}}, {}),
                         "array[uuid]")


class GoldenV1Adapter(unittest.TestCase):
    def route_fact(self, path, handler="m.py::h"):
        return {"id": "r1", "kind": "route", "confidence": "exact", "evidence": [{"path": "m.py", "start_line": 1}],
                "attributes": {"method": known("GET"), "handler": known(handler),
                               "path": known(path) if path else {"state": "unknown"},
                               "request_model_ids": known([]), "response_model_ids": known([])}}

    def test_http_call_inside_the_gold_span_matches(self):
        gold = {"routes": [], "external_calls": [
            {"system_kind": "http_api", "library": "httpx", "file": "a.py", "line_from": 47, "line_to": 49}]}
        result = result_of(dict(http_fact("f1", "GET"), evidence=[{"path": "a.py", "start_line": 49}]))
        h = fr029_golden4.compare(result, gold)["http_api"]
        self.assertEqual((h["tp"], len(h["fp"]), len(h["fn"])), (1, 0, 0))

    def test_non_http_library_is_outside_fr029_http(self):
        gold = {"routes": [], "external_calls": [
            {"system_kind": "http_api", "library": "fastapi_oauth20", "file": "g.py", "line_from": 21, "line_to": 21}]}
        h = fr029_golden4.compare(result_of(), gold)["http_api"]
        self.assertEqual((h["tp"], len(h["fn"]), h["out_of_scope"]), (0, 0, 1))

    def test_prefix_placeholder_matches_an_unknown_path(self):
        gold = {"routes": [{"method": "GET", "path": "/api/v1/sys{prefix}/all", "handler": "m.py::h",
                            "request_model": None, "response_model": None}], "external_calls": []}
        r = fr029_golden4.compare(result_of(self.route_fact(None)), gold)["routes"]
        self.assertEqual((r["tp"], len(r["fp"]), len(r["fn"])), (1, 0, 0))

    def test_prefix_placeholder_also_matches_the_resolved_prefix(self):
        gold = {"routes": [{"method": "GET", "path": "/api/v1/sys{prefix}/all", "handler": "m.py::h",
                            "request_model": None, "response_model": None}], "external_calls": []}
        r = fr029_golden4.compare(result_of(self.route_fact("/api/v1/sys/configs/all")), gold)["routes"]
        self.assertEqual((r["tp"], len(r["fp"]), len(r["fn"])), (1, 0, 0))
        r = fr029_golden4.compare(result_of(self.route_fact("/api/v1/other/all")), gold)["routes"]
        self.assertEqual((r["tp"], len(r["fp"]), len(r["fn"])), (0, 1, 1))

    def test_generic_response_name_has_its_arguments(self):
        page = {"id": "m1", "kind": "model", "attributes": {"name": known("PaginatedListResponse")}}
        item = {"id": "m2", "kind": "model", "attributes": {"name": known("APIKeyRead")}}
        route = self.route_fact("/k")
        route["attributes"]["response_model_ids"] = known(["m1"])
        route["attributes"]["bodies"] = known([{"direction": "response", "model_id": "m1",
                                                "type_args": [{"x-model-fact": "m2"}]}])
        gold = {"routes": [{"method": "GET", "path": "/k", "handler": "m.py::h", "request_model": None,
                            "response_model": "PaginatedListResponse[APIKeyRead]"}], "external_calls": []}
        rep = fr029_golden4.compare(result_of(page, item, route), gold)
        self.assertEqual(rep["models_on_matched_routes"]["wrong"], [])

    def test_golden_v1_gives_a_verdict_per_fact_for_exact(self):
        ok = self.route_fact("/a")
        bad = dict(self.route_fact("/b", "m.py::b"), id="r2")
        extra = dict(self.route_fact("/c", "m.py::c"), id="r3")
        gold = {"routes": [{"method": "GET", "path": "/a", "handler": "m.py::h", "request_model": None, "response_model": None},
                           {"method": "GET", "path": "/b", "handler": "m.py::b", "request_model": None,
                            "response_model": "Item"}], "external_calls": []}
        result = result_of(ok, bad, extra)
        rep = fr029_golden4.compare(result, gold)
        self.assertEqual(rep["facts"], {"r1": "ok", "r2": "wrong", "r3": "wrong"})
        ex = fr029_accept.exact_wrong(result, rep)
        self.assertEqual((ex["exact_facts"], ex["exact_wrong"]), (3, 2))

    def test_library_generic_response_name(self):
        item = {"id": "m2", "kind": "model", "attributes": {"name": known("APIKeyRead")}}
        route = self.route_fact("/k")
        route["attributes"]["response_type"] = known({"schema": {"type": "object", "x-external-model":
                                                                 "fastcrud.PaginatedListResponse",
                                                                 "x-type-args": [{"x-model-fact": "m2"}]}})
        gold = {"routes": [{"method": "GET", "path": "/k", "handler": "m.py::h", "request_model": None,
                            "response_model": "PaginatedListResponse[APIKeyRead]"}], "external_calls": []}
        self.assertEqual(fr029_golden4.compare(result_of(item, route), gold)["models_on_matched_routes"]["wrong"], [])

    def test_dict_types_compare_by_kind(self):
        self.assertEqual(fr029_golden4._short("dict[str, Any]"), fr029_golden4._short("dict"))

    def test_errata_fix_the_audited_values_without_touching_the_file(self):
        gold = {"routes": [{"method": "DELETE", "path": "/k", "handler": "backend/src/modules/api_keys/routes.py::delete_api_key",
                            "request_model": None, "response_model": "None"}], "external_calls": []}
        fixed = fr029_golden4.apply_errata("igorbenav-FastAPI-boilerplate", gold, check=False)
        self.assertIsNone(fixed["routes"][0]["response_model"])
        self.assertEqual(gold["routes"][0]["response_model"], "None")
        self.assertTrue(fixed["errata_applied"])

    def test_one_router_under_two_apps_counts_twice(self):
        gold = {"facts": [{"kind": "route", "source_id": "r.py::c", "attributes": {"method": "GET", "path": "/o"}}] * 2}
        want = fr029_golden_routes.gold_routes(gold)
        merged = fr029_golden_routes.our_routes(result_of(self.route_fact("/o", "r.py::c")))
        self.assertEqual(fr029_golden_routes.count(merged, want), (1, 0, 1))

    def test_dev_case_routes_are_scored_inside_the_declared_scope(self):
        manifest = {"scored_scope": {"exhaustive": {"route": ["src/case/views.py"]}}}
        got = {("GET", "/a", "src/case/views.py::a"), ("GET", "/healthcheck", "src/api.py::health")}
        want = {("GET", "/a", "src/case/views.py::a")}
        got_in, want_in, outside = fr029_golden_routes.in_scope(got, want, manifest)
        self.assertEqual((got_in, want_in, outside), (want, want, 1))


class MergeKey(unittest.TestCase):
    def test_different_fields_on_one_line_do_not_agree(self):
        a = {"fixture": "s", "kind": "model", "item": "T", "evidence": "m.py:10", "field": "fields.foo.required"}
        b = dict(a, field="fields.bar.nullable")
        self.assertNotEqual(fr029_grade_merge.key(a), fr029_grade_merge.key(b))


class Verdict(unittest.TestCase):
    def test_threshold_uses_raw_counts_and_zero_denominator_is_not_evaluated(self):
        row = {"kinds": {"routes": fr029_accept.rates(8, 2, 2), "models": fr029_accept.rates(0, 0, 0)},
               "exact": {"exact_facts": 20, "exact_wrong": 1, "rate": 0.05}}
        v = fr029_accept.verdict(row)
        self.assertEqual(v["routes"], "đạt")
        self.assertEqual(v["models"], "not_evaluated")
        self.assertEqual(v["exact"], "đạt")
        self.assertEqual(v["overall"], "chưa đủ đo")
        row["kinds"]["routes"] = fr029_accept.rates(7, 2, 2)  # P = 7/9 < 0.80
        self.assertEqual(fr029_accept.verdict(row)["routes"], "không đạt")


if __name__ == "__main__":
    unittest.main()
