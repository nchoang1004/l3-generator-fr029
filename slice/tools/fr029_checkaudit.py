"""Offline audit of the FR-029 checker (docfacts.Claims) on every repository that has an independent gold.

    python slice/tools/fr029_checkaudit.py --out DIR

No model is called. For each gold item the audit asks the checker two questions:
- false rejection: is a claim the gold says is true refused?
- false acceptance: is the same claim, made wrong on purpose (other method, other name, other URL), accepted?
It also measures the dependency-parameter reminders against the gold parameters, counts suspect lines (lines the
agent must account for) that are not gold items, and times the checker. The answers come from the gold files, never
from this code; the mutations are fixed rules listed in MUTATIONS, so every repository is tested the same way.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from l3slice import astscan, snapshot  # noqa: E402
from l3slice.docfacts import METHODS, Claims  # noqa: E402
from l3slice.source_tools import SourceTools  # noqa: E402

ACCEPT = "D:/VSF/l3-acceptance-gold"
REPOS = "D:/VSF/l3-acceptance-repos"
V1 = "D:/VSF/l3-generator-golden-v2"
DEV = Path("D:/VSF/VSF-L3 Generator")
FIX = HERE.parent / "tests" / "fixtures"
HELDOUT2_GOLD = "D:/VSF/l3-heldout-gold2"
HELDOUT2_REPOS = "D:/VSF/l3-heldout-repos2"
HTTP_LIBS = {"httpx", "requests", "aiohttp"}
MUTATIONS = {
    "route": "method không có trong decorator; handler là hàm route có thật khác của cùng file; tên handler không có",
    "route_negative": "route gold ghi not_fastapi (receiver không phải FastAPI/APIRouter) phải bị từ chối",
    "dependency": "dependency có thật khác (dùng ở route khác của repo) không có trên dòng; tên không tồn tại",
    "http": "URL thêm '/x-audit'; URL cụt 1 ký tự; literal khác có trong cùng file; thư viện khác; method khác",
    "http_negative": "dòng gold ghi non_http_calls (dict.get, Session.get, BeautifulSoup) nộp như lời gọi HTTP phải bị từ chối",
    "sanity": "chạy lại với bộ kiểm giả 'luôn nhận' và 'luôn từ chối': phép đo phải báo lỗi lớn"}


def fr029_cases() -> list[dict]:
    out = []
    for name, folder, gold in (("tdd-docker", "testdrivenio_fastapi-tdd-docker-16433b6", "tdd-docker/gold.json"),
                               ("agentgpt", "reworkd_AgentGPT-18b073a", "agentgpt/gold.r2.json"),
                               ("kibo", "KIBO-Agenda_kibo-backend-89eb3bb", "kibo/gold.r2.json")):
        g = json.loads(Path(ACCEPT, gold).read_text(encoding="utf-8"))
        out.append({"name": name, "group": "nghiệm thu", "src": Path(REPOS, folder, g.get("root", ".")), "gold": g, "fmt": "fr029"})
    for gp in sorted(Path(HELDOUT2_GOLD).glob("*/gold.json")):  # new repositories, gold by two independent writers
        g = json.loads(gp.read_text(encoding="utf-8"))
        out.append({"name": "new/" + gp.parent.name, "group": "repo mới", "src": Path(HELDOUT2_REPOS, gp.parent.name,
                                                                                    g.get("root", ".")),
                    "gold": g, "fmt": "fr029"})
    for gp in sorted((FIX / "fr029").glob("*.gold.json")) + [FIX / "fr029_e2e.gold.json"]:
        g = json.loads(gp.read_text(encoding="utf-8"))
        src = gp.parent / gp.name.replace(".gold.json", "")
        out.append({"name": "fixture/" + src.name, "group": "fixture", "src": src, "gold": g, "fmt": "fr029"})
    return out


def v1_cases() -> list[dict]:
    out = []
    for folder, answer, src in (("teamhide-fastapi-boilerplate", "final-r3.json", "teamhide_fastapi-boilerplate-df4e6d4"),
                                ("full-stack-fastapi-template", "final-r2.json", "full-stack-fastapi-template-cb740b6"),
                                ("igorbenav-FastAPI-boilerplate", "final-r3.json", "fastapi-boilerplate"),
                                ("fastapi_best_architecture", "final-r2.json",
                                 "fastapi-practices_fastapi_best_architecture-123a44a")):
        g = json.loads(Path(V1, ".aide/evidence/tests/golden-v1", folder, answer).read_text(encoding="utf-8"))
        out.append({"name": folder, "group": "golden v1", "src": Path(V1, "sample-repos", src), "gold": g, "fmt": "v1"})
    manifest = json.loads((DEV / "evaluation/golden/v1/manifest.json").read_text(encoding="utf-8"))
    for case in manifest["cases"]:
        if case["split"] != "development" or case["family"] not in ("fastapi-docs", "orders-fixture", "netflix-dispatch"):
            continue
        g = json.loads((DEV / case["case"] / "gold.json").read_text(encoding="utf-8"))
        out.append({"name": "dev/" + case["case_id"], "group": "ca dev", "src": DEV / case["source"], "gold": g, "fmt": "dev"})
    return out


def gold_routes(case) -> list[dict]:
    """(method, handler 'file::func') of every gold route; dev gold has the file inside source_id."""
    g = case["gold"]
    if case["fmt"] == "fr029":
        return [{"method": r["method"], "handler": r["handler"], "path": r.get("path")} for r in g.get("routes", [])
                if r.get("handler")]
    if case["fmt"] == "v1":
        return [{"method": r["method"], "handler": r["handler"]} for r in g["routes"] if r["method"] in METHODS]
    return [{"method": f["attributes"]["method"], "handler": f["source_id"]} for f in g["facts"] if f["kind"] == "route"]


def claims_for(src: Path):
    snap, sources = snapshot.take(src)
    tools = SourceTools(snap, sources)
    for p in tools.readable:  # the audit plays an agent that has read every line
        for i in range(1, len(tools.lines[p]) + 1):
            tools.state[p][i] = "processed"
    return Claims(tools), tools


def function_node(tools, handler):
    path, name = handler.split("::")
    if path not in tools.raw:
        return None, None
    try:
        tree = ast.parse(tools.raw[path])
    except (SyntaxError, ValueError):
        return path, None
    nodes = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name
             and n.decorator_list]
    return path, nodes


def audit_routes(case, claims, tools) -> dict:
    """True claims must pass; every mutation runs whether or not the true claim passed (counted in `mutations`)."""
    res = {"checked": 0, "false_rejection": [], "false_acceptance": [], "not_found": [], "mutations": 0,
           "negatives": 0, "negative_accepted": []}
    seen = set()
    for r in gold_routes(case):
        key = (r["method"], r["handler"])
        if key in seen:
            continue
        seen.add(key)
        path, nodes = function_node(tools, r["handler"])
        if not nodes:
            res["not_found"].append(r["handler"])
            continue
        res["checked"] += 1
        decs = [(path, min(d.lineno for d in n.decorator_list), n.lineno) for n in nodes]
        hits = [d for d in decs if not claims._decorator_problems(d, r["handler"], r["method"])]
        if not hits:
            res["false_rejection"].append({"route": f"{r['method']} {r['handler']}",
                                           "why": claims._decorator_problems(decs[0], r["handler"], r["method"])})
        dec = (hits or decs)[0]
        text = "\n".join(tools.lines[path][dec[1] - 1:dec[2]])
        wrong = next(m for m in ("PATCH", "PUT", "DELETE", "GET", "POST", "HEAD")
                     if not re.search(rf"\.{m.lower()}\s*\(|['\"]{m}['\"]", text))
        others = [n.name for n in ast.walk(ast.parse(tools.raw[path])) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                  and n.decorator_list and n.name != r["handler"].split("::")[1]]
        # path: the literal of this route's own decorator (read here from the syntax tree) must pass; the literal of
        # another function's decorator must not
        own = [n for n in nodes if (path, min(x.lineno for x in n.decorator_list), n.lineno) == dec]
        true_lits = {d.args[0].value for n in own for d in n.decorator_list if isinstance(d, ast.Call)
                     and isinstance(d.func, ast.Attribute) and d.func.attr == r["method"].lower() and d.args
                     and isinstance(d.args[0], ast.Constant) and isinstance(d.args[0].value, str)}
        other_lits = {d.args[0].value for n in ast.walk(ast.parse(tools.raw[path])) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                  and n not in own for d in n.decorator_list if isinstance(d, ast.Call) and d.args
                  and isinstance(d.args[0], ast.Constant) and isinstance(d.args[0].value, str)} - true_lits
        mine = claims._decorator_paths(dec, r["method"])
        mine = mine if mine is not None else set()
        if true_lits and not all(t in mine for t in true_lits):
            res["false_rejection"].append({"route": f"{r['method']} {r['handler']}", "why": f"path {sorted(true_lits)}"})
        wrong_path = sorted(other_lits)[0] if other_lits else None
        if wrong_path is not None:
            res["mutations"] += 1
            if wrong_path in mine:
                res["false_acceptance"].append({"route": f"{r['method']} {r['handler']}", "mutation": f"path {wrong_path}"})
        for label, handler, method in (("method " + wrong, r["handler"], wrong),
                                       ("handler của route khác", f"{path}::{others[0]}" if others else None, r["method"]),
                                       ("handler không tồn tại", f"{path}::khong_co_ham_nay", r["method"])):
            if handler is None:
                continue
            res["mutations"] += 1
            if not claims._decorator_problems(dec, handler, method):
                res["false_acceptance"].append({"route": f"{r['method']} {r['handler']}", "mutation": label})
    # registration: a route the gold says is served must hang below at least one FastAPI app of the snapshot;
    # the checker must never conclude "not registered" for it
    apps = []
    for p in tools.readable:
        if p.endswith(".py"):
            for i, line in enumerate(tools.lines[p], 1):
                if re.match(r"\s*\w+\s*(?::[^=]*)?=\s*(?:fastapi\.)?FastAPI\s*\(", line):
                    apps.append((p, i, i))
    res["registration_checked"] = 0
    res["registration_false_rejection"] = []
    res.update(prefix_mutations=0, prefix_missing_accepted=[], prefix_none_checked=0, prefix_none_rejected=[])
    if apps:
        for r in gold_routes(case):
            path, nodes = function_node(tools, r["handler"])
            if not nodes:
                continue
            node = nodes[0]
            dec = (path, min(x.lineno for x in node.decorator_list), node.lineno)
            res["registration_checked"] += 1
            verdicts = [claims._registration_problems(dec, app, []) for app in apps]
            if all(any("không được include_router" in e for e in v) for v in verdicts):
                res["registration_false_rejection"].append(f"{r['method']} {r['handler']}")
            # prefix: the gold path minus this decorator's literal (read here) is what include_router/APIRouter add.
            # A claim citing only the decorator must pass when nothing is added, and fail on every app otherwise.
            own = [(d.lineno, d.args[0].value) for d in node.decorator_list if isinstance(d, ast.Call)
                   and isinstance(d.func, ast.Attribute) and d.func.attr == r["method"].lower() and d.args
                   and isinstance(d.args[0], ast.Constant) and isinstance(d.args[0].value, str)]
            if not r.get("path") or len(own) != 1 or not r["path"].endswith(own[0][1]):
                continue
            added = r["path"][:len(r["path"]) - len(own[0][1])]
            parts = [{"kind": "decorator", "value": own[0][1], "at": (path, own[0][0], own[0][0])}]
            # a route declared on a FastAPI app itself (@app.get, @sub_app.get mounted under /sub) has no router
            # prefix to measure; the name is matched against the app lines, which may skip a few routers too
            receiver = next(_name(d.func.value) for d in node.decorator_list if isinstance(d, ast.Call)
                            and isinstance(d.func, ast.Attribute) and d.func.attr == r["method"].lower())
            if any(re.match(rf"\s*{re.escape(receiver or '')}\s*(?::[^=]*)?=", tools.lines[a[0]][a[1] - 1])
                   for a in apps):
                continue
            verdicts = [claims._registration_problems(dec, app, parts) for app in apps]
            if added.strip("/"):
                res["prefix_mutations"] += 1
                if any(not v for v in verdicts):
                    res["prefix_missing_accepted"].append(f"{r['method']} {r['path']} (thiếu {added})")
            else:
                res["prefix_none_checked"] += 1
                if all(v for v in verdicts):
                    res["prefix_none_rejected"].append(f"{r['method']} {r['path']}: {verdicts[0]}")
    for x in case["gold"].get("excluded_routes", []):
        if x.get("reason") != "not_fastapi":
            continue  # tests and out-of-scope folders are excluded by scope, not by the decorator check
        path, line = x["where"].rsplit(":", 1)
        tree = ast.parse(tools.raw[path])
        node = next(n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and any(d.lineno == int(line) for d in n.decorator_list))
        verb = re.search(r"\.(get|post|put|patch|delete)\s*\(", tools.lines[path][int(line) - 1]).group(1).upper()
        res["negatives"] += 1
        if not claims._decorator_problems((path, int(line), node.lineno), f"{path}::{node.name}", verb):
            res["negative_accepted"].append(x["where"])
    return res


def alias_table(tools) -> dict:
    """(file, alias) -> dependency names wrapped by `Alias = Annotated[..., Depends(f)]`. Written separately from the
    checker's own alias reading on purpose, so the audit does not take the checker's answer as the expected one."""
    table = {}
    for path in tools.readable:
        if not path.endswith(".py"):
            continue
        try:
            tree = ast.parse(tools.raw[path])
        except (SyntaxError, ValueError):
            continue
        for n in tree.body:
            target = n.targets[0] if isinstance(n, ast.Assign) and len(n.targets) == 1 else getattr(n, "target", None)
            value = getattr(n, "value", None)  # only Annotated[...] values are read as text (get_source_segment is slow)
            text = ast.get_source_segment(tools.raw[path], value) or "" if isinstance(
                n, (ast.Assign, ast.AnnAssign)) and isinstance(value, ast.Subscript) else ""
            if isinstance(target, ast.Name) and text.lstrip().startswith(("Annotated[", "typing.Annotated[")):
                names = re.findall(r"(?:Depends|Security)\(\s*([\w.]+)", text)
                if names:
                    table[(path, target.id)] = names
    return table


def resolve_alias(table, tools, path, name) -> list[str]:
    """The alias as the handler's file sees it: defined there, imported from a module, or the only definition."""
    if (path, name) in table:
        return table[(path, name)]
    m = re.search(rf"^\s*from\s+([\w.]+)\s+import\s+[^\n]*\b{re.escape(name)}\b", tools.raw[path], re.M)
    if m:
        tail = m.group(1).replace(".", "/")
        hits = [k for k in table if k[1] == name and (k[0].endswith(tail + ".py") or k[0].endswith(tail + "/__init__.py"))]
        if len(hits) == 1:
            return table[hits[0]]
    hits = [k for k in table if k[1] == name]
    return table[hits[0]] if len(hits) == 1 else []


def route_dependencies(node, claims, path=None, table=None) -> list[tuple[str, int]]:
    """(dependency name, line) of a handler: Depends/Security in defaults or Annotated, Annotated aliases, and
    dependencies=[...] of its decorators. Router and app level dependencies are not followed (reported apart)."""
    out = []
    tools = claims.tools
    table = alias_table(tools) if table is None else table
    a = node.args
    pos = a.posonlyargs + a.args
    pairs = list(zip(pos, [None] * (len(pos) - len(a.defaults)) + list(a.defaults))) + list(zip(a.kwonlyargs, a.kw_defaults))

    def dep_of(e):
        if isinstance(e, ast.Call) and _name(e.func) in ("Depends", "Security") and e.args:
            t = e.args[0].func if isinstance(e.args[0], ast.Call) else e.args[0]
            return ast.unparse(t) if isinstance(t, ast.Attribute) else _name(t)  # Crud.inject as the agent writes it
        return None

    for arg, default in pairs:
        exprs = [default]
        ann = arg.annotation
        if isinstance(ann, ast.Subscript) and _name(ann.value) == "Annotated" and isinstance(ann.slice, ast.Tuple):
            exprs += ann.slice.elts[1:]
        if isinstance(ann, ast.Name):
            out += [(d, arg.lineno, arg.lineno) for d in resolve_alias(table, tools, path, ann.id)] if path else []
        # an agent cites the lines of the parameter, which may run over several lines: Depends(\n f(...))
        out += [(dep_of(e), arg.lineno, e.end_lineno) for e in exprs if dep_of(e)]
        typ = ann.slice.elts[0] if len(exprs) > 1 else ann  # Annotated[Filters, Depends()]: its first element
        if isinstance(typ, (ast.Name, ast.Attribute)) and any(  # f: Filters = Depends(): the annotation is the dependency
                isinstance(e, ast.Call) and _name(e.func) in ("Depends", "Security") and not e.args for e in exprs):
            out.append((ast.unparse(typ) if isinstance(typ, ast.Attribute) else typ.id, arg.lineno, arg.lineno))
    for dec in node.decorator_list:
        for kw in getattr(dec, "keywords", []):
            if kw.arg == "dependencies" and isinstance(kw.value, (ast.List, ast.Tuple)):
                out += [(dep_of(e), e.lineno, e.end_lineno) for e in kw.value.elts if dep_of(e)]
    return out


def _name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _key(place, name):
    """HTTP names on both sides: header case does not matter, but x_custom and x-custom are different headers."""
    return (place, name.lower() if place == "header" else name)


def handler_keys(node, tools, path, table) -> set:
    """HTTP parameters the handler declares itself (not through Depends/Security): name, alias, header form."""
    keys = set()
    a = node.args
    args = a.posonlyargs + a.args
    pairs = list(zip(args, [None] * (len(args) - len(a.defaults)) + list(a.defaults))) + list(zip(a.kwonlyargs, a.kw_defaults))
    for arg, default in pairs:
        ann = arg.annotation
        exprs = [default] + (list(ann.slice.elts[1:]) if isinstance(ann, ast.Subscript) and isinstance(ann.slice, ast.Tuple)
                             else [])
        names = {_name(e.func) for e in exprs if isinstance(e, ast.Call)}
        if names & {"Depends", "Security"} or (isinstance(ann, ast.Name) and resolve_alias(table, tools, path, ann.id)):
            continue
        place = next((m.lower() for m in ("Header", "Query", "Cookie", "Path") if m in names), None)
        call = next((e for e in exprs if isinstance(e, ast.Call) and _name(e.func) in ("Header", "Query", "Cookie", "Path")), None)
        alias = next((k.value.value for k in getattr(call, "keywords", []) if k.arg == "alias"
                      and isinstance(k.value, ast.Constant)), None)
        convert = not any(k.arg == "convert_underscores" and getattr(k.value, "value", True) is False
                          for k in getattr(call, "keywords", []))
        name = alias or (arg.arg.replace("_", "-") if place == "header" and convert else arg.arg)
        for pl in ([place] if place else ["query", "path"]):
            keys.add(_key(pl, name))
    return keys


def audit_dependencies(case, claims, tools) -> dict:
    """Reminders as the agent receives them: routes holding only their dependencies go through open_problems; the
    parameters the gold lists and the handler does not declare itself are the expected reminders."""
    res = {"routes": 0, "dependency_lines": 0, "dependency_false_rejection": [], "dependency_false_acceptance": [],
           "mutations": 0, "measured": case["fmt"] == "fr029",
           "reminders": 0, "reminders_wrong": [], "gold_dep_params": 0, "missed": []}
    routes = {(r["method"], r["handler"]): r for r in case["gold"].get("routes", [])} if case["fmt"] == "fr029" else {}
    table = alias_table(tools)
    found = {}
    all_deps = set()
    for key, r in sorted(routes.items()):
        path, nodes = function_node(tools, key[1])
        if nodes:
            found[key] = (path, nodes[0], route_dependencies(nodes[0], claims, path, table))
            all_deps |= {d for d, _, _ in found[key][2]}
    probe = Claims(tools)  # a fresh checker holding only these routes and their dependencies
    for (method, handler), (path, node, deps) in found.items():
        r = routes[(method, handler)]
        res["routes"] += 1
        for d, line, end in deps:  # the checker must accept every true dependency line, refuse a name not on it
            res["dependency_lines"] += 1
            if not claims.dependency_at(d, (path, line, end)):
                res["dependency_false_rejection"].append(f"{handler} {d} @ {path}:{line}-{end}")
            res["mutations"] += 1
            if claims.dependency_at("khong_co_dependency_nay", (path, line, end)):
                res["dependency_false_acceptance"].append(f"{handler} @ {path}:{line} (tên không tồn tại)")
            span = "\n".join(tools.lines[path][line - 1:end])
            other = next((o for o in sorted(all_deps) if o.split(".")[-1] != d.split(".")[-1]
                          and not re.search(rf"\b{re.escape(o.split('.')[-1])}\b", span)
                          and not any(o in table.get(k, []) for k in table if k[1] in span)), None)
            if other:
                res["mutations"] += 1
                if claims.dependency_at(other, (path, line, end)):
                    res["dependency_false_acceptance"].append(f"{handler} @ {path}:{line} ({other})")
        dec = (path, min(x.lineno for x in node.decorator_list), node.lineno)
        probe.routes[(handler, method, None, ())] = {
            "method": method, "handler": handler, "decorator": dec, "application": None, "application_unknown": None,
            "parts": [{"kind": "decorator", "value": r.get("path") or "", "at": dec, "used_at": None}],
            "params": [], "body": None, "response": None, "status": None, "auth": None,
            "dependencies": [{"name": dn, "at": (path, line, end)} for dn, line, end in deps]}
    told = {}
    for msg in probe.open_problems([]):
        m = re.match(r"Route (\S+) (\S+): dependency \S+ khai tham số (\w+) '([^']+)' tại (\S+);", msg)
        if m:
            told.setdefault((m.group(1), m.group(2)), {})[_key(m.group(3), m.group(4))] = m.group(5)
    for (method, handler), (path, node, deps) in found.items():
        r = routes[(method, handler)]
        reminded = told.get((method, handler), {})
        gold = {_key(p["in"], p["name"]) for p in r.get("params", []) if p["in"] in ("header", "query", "cookie", "path")}
        res["reminders"] += len(reminded)
        res["reminders_wrong"] += [f"{method} {handler}: {k[0]} {k[1]} ({at})" for k, at in reminded.items() if k not in gold]
        direct = handler_keys(node, tools, path, table)
        for k in sorted(gold - direct):
            if k[0] == "path" and _key("query", k[1]) in direct:
                continue
            res["gold_dep_params"] += 1
            if k not in reminded:
                res["missed"].append(f"{method} {handler}: {k[0]} {k[1]}")
    return res


def http_items(case) -> list[dict]:
    g = case["gold"]
    out = []
    if case["fmt"] == "fr029":
        for h in g.get("http_calls", []):
            t = h["target"]
            out.append({"where": h["where"], "alt": h.get("alt_where", []), "library": h["library"], "method": h["method"],
                        "literal": t.get("value") if t.get("kind") == "literal" else None})
    elif case["fmt"] == "v1":
        for x in g.get("external_calls", []):
            if x["system_kind"] == "http_api" and x.get("library") in HTTP_LIBS:
                url = x.get("target") or ""
                literal = url if url.startswith("http") and "{" not in url else None
                out.append({"where": f"{x['file']}:{x['line_from']}", "span": (x["line_from"], x["line_to"]),
                            "alt": [], "library": x["library"], "method": None, "literal": literal})
    return out


def audit_http(case, claims, tools) -> dict:
    res = {"calls": 0, "literal": 0, "false_rejection": [], "false_acceptance": [], "gold_vs_rule": [], "mutations": 0,
           "negatives": 0, "negative_accepted": []}
    for h in http_items(case):
        res["calls"] += 1
        path, line = h["where"].rsplit(":", 1)
        lines = [int(line)] + [int(a.rsplit(":", 1)[1]) for a in h["alt"]]
        if "span" in h:
            lines = list(range(h["span"][0], h["span"][1] + 1))
        call_line = next((n for n in lines if re.search(r"\.(get|post|put|patch|delete|head|options|request|stream|send)\s*\(",
                                                         tools.lines.get(path, [""] * n)[n - 1])), None)
        if call_line is None:
            res["false_rejection"].append({"call": h["where"], "why": "không thấy dòng có lời gọi trong đoạn gold"})
            continue
        verb = re.search(r"\.(get|post|put|patch|delete|head|options)\s*\(", tools.lines[path][call_line - 1])
        method = h["method"] or (verb.group(1).upper() if verb else None)
        if method is None:
            continue
        if method == "unknown":
            method = {"unknown": "method chỉ biết lúc chạy"}
        elif not verb and not re.search(r"\.(request|stream)\s*\(\s*['\"]", tools.lines[path][call_line - 1]):
            res["gold_vs_rule"].append({"call": h["where"], "gold_method": method})
            method = {"unknown": "method là biến"}
        target = {"kind": "literal", "value": h["literal"]} if h["literal"] else {"kind": "unknown", "reason": "audit"}
        item = {"at": f"{path}:{call_line}", "library": h["library"], "method": method, "target": target}
        errs = Claims(tools).add_http(item)
        if errs:
            res["false_rejection"].append({"call": item["at"], "target": target.get("value"), "why": errs})
        if h["literal"]:
            res["literal"] += 1
        mutations = []
        if h["literal"]:
            decoys = [v for v in re.findall(r"['\"](https?://[^'\"]+)['\"]", tools.raw[path]) if v != h["literal"]]
            mutations += [("URL thêm hậu tố", dict(item, target={"kind": "literal", "value": h["literal"] + "/x-audit"})),
                          ("URL cụt", dict(item, target={"kind": "literal", "value": h["literal"][:-1]}))]
            if decoys:
                mutations.append(("URL mồi trong file", dict(item, target={"kind": "literal", "value": decoys[0]})))
        mutations += [(f"thư viện {lib}", dict(item, library=lib)) for lib in sorted(HTTP_LIBS - {h["library"]})]
        if verb and isinstance(method, str):
            other = "DELETE" if method != "DELETE" else "PATCH"
            mutations.append((f"method {other}", dict(item, method=other)))
        for label, bad in mutations:
            res["mutations"] += 1
            if not Claims(tools).add_http(bad):
                res["false_acceptance"].append({"call": item["at"], "mutation": label})
    for x in case["gold"].get("non_http_calls", []) if case["fmt"] == "fr029" else []:
        path, line = x["where"].rsplit(":", 1)
        verb = re.search(r"\.(get|post|put|patch|delete)\s*\(", tools.lines[path][int(line) - 1])
        if not verb:
            continue
        res["negatives"] += 1
        for lib in sorted(HTTP_LIBS):
            bad = {"at": x["where"], "library": lib, "method": verb.group(1).upper(),
                   "target": {"kind": "unknown", "reason": "audit"}}
            if not Claims(tools).add_http(bad):
                res["negative_accepted"].append(f"{x['where']} ({lib})")
                break
    return res


def audit_suspects(case, claims, tools) -> dict:
    """Lines the checker makes the agent account for, against the gold routes and HTTP calls."""
    sus = claims.suspects()
    flagged = {(s["at"].rsplit(":", 1)[0], int(s["at"].rsplit(":", 1)[1])) for s in sus}
    accounted = set()  # limitations and excluded routes of the gold: lines the agent must explain, not noise
    for x in case["gold"].get("limitations", []) + case["gold"].get("excluded_routes", []):
        for w in [x.get("where") or x.get("declared_at"), *x.get("alt_where", [])]:
            if isinstance(w, str) and ":" in w:
                accounted.add((w.rsplit(":", 1)[0], int(w.rsplit(":", 1)[1])))
    route_lines = set()
    for r in gold_routes(case):
        path, nodes = function_node(tools, r["handler"])
        for n in nodes or []:
            route_lines |= {(path, d.lineno) for d in n.decorator_list}
    http_lines = set()
    for h in http_items(case):
        path, line = h["where"].rsplit(":", 1)
        span = h.get("span") or (int(line), int(line))
        http_lines |= {(path, i) for i in range(span[0], span[1] + 4)}
    noise = []
    for s in sus:
        path, line = s["at"].rsplit(":", 1)
        line = int(line)
        text = tools.lines[path][line - 1].strip()
        if (path, line) in route_lines or (path, line) in http_lines or (path, line) in accounted:
            continue
        noise.append({"at": s["at"], "looks_like": s["looks_like"], "text": text[:100]})
    # every gold route decorator and HTTP call must be flagged, or the agent can skip it unnoticed
    missed = []
    for r in gold_routes(case):
        path, nodes = function_node(tools, r["handler"])
        for n in nodes or []:
            decs = [(path, d.lineno) for d in n.decorator_list
                    if re.search(r"\.(get|post|put|patch|delete|head|options|trace|api_route|websocket)\s*\(",
                                 tools.lines[path][d.lineno - 1])]
            if decs and not any(x in flagged for x in decs):
                missed.append(f"route {r['handler']}")
    as_http = {(s["at"].rsplit(":", 1)[0], int(s["at"].rsplit(":", 1)[1])) for s in sus if s["looks_like"] == "http"}
    for h in http_items(case):
        path, line = h["where"].rsplit(":", 1)
        span = h.get("span") or (int(line), int(line))
        lines = set(range(span[0], span[1] + 1)) | {int(a.rsplit(":", 1)[1]) for a in h["alt"]}
        if not any((path, i) in as_http for i in lines):  # flagged as an HTTP call, not as some other kind
            missed.append(f"http {h['where']}")
    # a line holding k gold calls must stay flagged while the agent has claimed only k - 1 of them
    per_line = Counter(h["where"] for h in http_items(case) if "span" not in h)
    multi, multi_missed = 0, []
    for where, k in per_line.items():
        if k < 2:
            continue
        path, line = where.rsplit(":", 1)
        multi += 1
        fake = [(path, int(line), int(line), -1 - j) for j in range(k - 1)]  # k - 1 claims at that line
        for key in fake:
            claims.http[key] = {}
        try:
            if f"{path}:{line}" not in {s["at"] for s in claims.suspects()}:
                multi_missed.append(where)
        finally:
            for key in fake:
                claims.http.pop(key, None)
    return {"suspects": len(sus), "not_gold_item": len(noise), "examples": noise[:15],
            "gold_items": len(gold_routes(case)) + len(http_items(case)), "gold_not_flagged": missed,
            "multi_call_lines": multi, "multi_call_unflagged": multi_missed}


ROUTE_DECORATOR = re.compile(r"\.(get|post|put|patch|delete|head|options|trace)\s*\(")


def heldout_packet(src: Path) -> dict:
    """What the checker produces on a repository without gold, for an independent judge: the request parameters it
    finds for every Depends function used by a route, every suspect line, and how many real route decorators (method
    read from the decorator) it refuses. The judge decides what is right; nothing here is scored by this code."""
    t0 = time.time()
    claims, tools = claims_for(src)
    table = alias_table(tools)
    # dependencies an Annotated alias calls as a factory: Annotated[User, Depends(require_permission("admin"))]
    alias_called = {m.group(1).split(".")[-1] for p in tools.readable if p.endswith(".py")
                    for m in re.finditer(r"Annotated\[[^\n]*?(?:Depends|Security)\(\s*([\w.]+)\s*\(", tools.raw[p])}
    deps, refused, decorators = {}, [], 0
    for path in tools.readable:
        if not path.endswith(".py"):
            continue
        tree = astscan.parse(tools.raw[path])  # the checker's parser, Python 3.14 `except A, B:` included
        if tree is None:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or not node.decorator_list:
                continue
            for d in node.decorator_list:
                m = ROUTE_DECORATOR.search(tools.lines[path][d.lineno - 1])
                if not m or not tools.lines[path][d.lineno - 1].lstrip().startswith("@"):
                    continue
                decorators += 1
                dec = (path, min(x.lineno for x in node.decorator_list), node.lineno)
                problems = claims._decorator_problems(dec, f"{path}::{node.name}", m.group(1).upper())
                if problems:
                    refused.append({"at": f"{path}:{d.lineno}", "why": problems})
                for name, line, end in route_dependencies(node, claims, path, table):
                    span = "\n".join(tools.lines[path][line - 1:end])  # Depends(f(...)) read here, as in the audit
                    called = bool(re.search(rf"(?<![\w.]){re.escape(name)}\s*\(", span))
                    if not called and not re.search(rf"(?<![\w.]){re.escape(name)}\b", span):
                        called = name in alias_called  # u: ManageUser, the alias holds Depends(f(...))
                    params = [{"in": pl, "name": n, "at": at}
                              for pl, n, at in claims.dependency_params(name, set(), called, path)]
                    # one entry per distinct answer: same-named functions of several modules stay apart
                    key = (name, called, json.dumps(params, sort_keys=True))
                    if key not in deps:
                        deps[key] = {"name": name, "called": called, "first_use": f"{path}:{line}", "params": params}
    suspects = [s for s in claims.suspects() if s["looks_like"] != "route"
                or not ROUTE_DECORATOR.search(tools.lines[s["at"].rsplit(":", 1)[0]][int(s["at"].rsplit(":", 1)[1]) - 1])]
    for s in suspects:
        path, line = s["at"].rsplit(":", 1)
        s["text"] = tools.lines[path][int(line) - 1].strip()[:160]
    return {"repository": str(src), "files": len(tools.readable), "route_decorators": decorators,
            "decorators_refused": refused, "dependencies": list(deps.values()), "suspects": suspects,
            "seconds": round(time.time() - t0, 2)}


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--sanity", choices=["accept", "reject"],
                   help="thay bộ kiểm bằng bản giả luôn nhận/luôn từ chối, để thấy phép đo có phân biệt được không")
    p.add_argument("--heldout", nargs="*", type=Path, default=[],
                   help="repo không có gold: chỉ xuất gói cho giám khảo độc lập chấm")
    a = p.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    if a.sanity:
        everything = a.sanity == "accept"
        Claims._decorator_problems = lambda self, *x: [] if everything else ["giả"]
        Claims.add_http = lambda self, item: [] if everything else ["giả"]
        Claims.dependency_at = lambda self, *x: everything
        Claims._registration_problems = lambda self, *x: [] if everything else ["giả: không được include_router"]

        class _Every(set):
            def __contains__(self, item):
                return True
        Claims._decorator_paths = lambda self, *x: _Every() if everything else set()
        Claims.dependency_params = (lambda self, *x, **k: [("query", "zzz_gia", "x:1")]) if everything \
            else (lambda self, *x, **k: [])
        Claims.suspects = (lambda self: [{"at": f"{q}:{i}", "looks_like": "http"} for q in self.tools.readable
                                         for i in range(1, len(self.tools.lines[q]) + 1)]) if everything \
            else (lambda self: [])
    if a.heldout:
        for src in a.heldout:
            packet = heldout_packet(src)
            (a.out / f"{src.name}.packet.json").write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"{src.name}: {packet['route_decorators']} decorator, {len(packet['decorators_refused'])} bị từ chối, "
                  f"{len(packet['dependencies'])} dependency, {len(packet['suspects'])} dòng nghi ngờ, {packet['seconds']}s")
        return 0
    rows = []
    for case in fr029_cases() + v1_cases():
        t0 = time.time()
        row = {"case": case["name"], "group": case["group"]}
        try:
            claims, tools = claims_for(case["src"])
            row["files"] = len(tools.readable)
            row["routes"] = audit_routes(case, claims, tools)
            row["dependencies"] = audit_dependencies(case, claims, tools)
            row["http"] = audit_http(case, claims, tools)
            row["suspects"] = audit_suspects(case, claims, tools)
        except Exception as exc:  # recorded: a crash of the checker is a finding
            row["error"] = f"{type(exc).__name__}: {exc}"
        row["seconds"] = round(time.time() - t0, 2)
        rows.append(row)
        print(f"{case['name']}: {row.get('error') or 'ok'} ({row['seconds']}s)", file=sys.stderr, flush=True)
    (a.out / "audit.json").write_text(json.dumps({"mutations": MUTATIONS, "rows": rows}, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    total = lambda k, f: sum(len(r.get(k, {}).get(f, [])) if isinstance(r.get(k, {}).get(f), list)  # noqa: E731
                             else r.get(k, {}).get(f, 0) for r in rows)
    import hashlib
    digest = lambda f: hashlib.sha256(Path(f).read_bytes()).hexdigest()[:16]  # noqa: E731
    versions = {"docfacts.py": digest(HERE.parent / "l3slice/docfacts.py"),
                "astscan.py": digest(HERE.parent / "l3slice/astscan.py"), "fr029_checkaudit.py": digest(__file__)}
    summary = {
        "versions": versions, "sanity": a.sanity or "không", "cases": len(rows), "errors": [r["case"] for r in rows if "error" in r],
        "route_mutations": total("routes", "mutations"), "route_negatives": total("routes", "negatives"),
        "route_negative_accepted": total("routes", "negative_accepted"),
        "dependency_mutations": total("dependencies", "mutations"),
        "dependency_cases_measured": sum(1 for r in rows if r.get("dependencies", {}).get("measured")),
        "http_mutations": total("http", "mutations"), "http_negatives": total("http", "negatives"),
        "http_negative_accepted": total("http", "negative_accepted"),
        "routes_checked": total("routes", "checked"), "routes_false_rejection": total("routes", "false_rejection"),
        "routes_false_acceptance": total("routes", "false_acceptance"), "routes_not_found": total("routes", "not_found"),
        "registration_checked": total("routes", "registration_checked"),
        "registration_false_rejection": total("routes", "registration_false_rejection"),
        "prefix_mutations": total("routes", "prefix_mutations"),
        "prefix_missing_accepted": total("routes", "prefix_missing_accepted"),
        "prefix_none_checked": total("routes", "prefix_none_checked"),
        "prefix_none_rejected": total("routes", "prefix_none_rejected"),
        "dependency_lines": total("dependencies", "dependency_lines"),
        "dependency_false_rejection": total("dependencies", "dependency_false_rejection"),
        "dependency_false_acceptance": total("dependencies", "dependency_false_acceptance"),
        "reminders": total("dependencies", "reminders"), "reminders_wrong": total("dependencies", "reminders_wrong"),
        "gold_dep_params": total("dependencies", "gold_dep_params"), "dep_params_missed": total("dependencies", "missed"),
        "http_calls": total("http", "calls"), "http_false_rejection": total("http", "false_rejection"),
        "http_literal_checked": total("http", "literal"), "http_false_acceptance": total("http", "false_acceptance"),
        "http_gold_vs_rule": total("http", "gold_vs_rule"),
        "suspects": total("suspects", "suspects"), "suspects_not_gold_item": total("suspects", "not_gold_item"),
        "gold_items_for_suspects": total("suspects", "gold_items"),
        "gold_items_not_flagged": total("suspects", "gold_not_flagged"),
        "multi_call_lines": total("suspects", "multi_call_lines"),
        "multi_call_unflagged": total("suspects", "multi_call_unflagged")}
    (a.out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
