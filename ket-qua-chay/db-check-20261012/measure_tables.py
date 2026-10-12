"""Đo phần bảng CSDL (FR-030) với gold golden-v1: bảng, cột, khóa chính, khóa ngoại, nullable, kiểu. Không gọi model.
Chạy từ gốc repo. In số đo và mọi chỗ lệch."""
import json
import re
import sys
from collections import Counter

sys.path[:0] = ["slice", "slice/tools"]
import fr029_checkaudit as A  # noqa: E402
from l3slice import snapshot  # noqa: E402
from l3slice.common import is_known  # noqa: E402
from l3slice.docstatic import declared, static_facts  # noqa: E402
from l3slice.source_tools import SourceTools  # noqa: E402


def v(field):
    return field.get("value") if isinstance(field, dict) and field.get("state") == "known" else None


def code_type(col):
    t = col.get("type") or {}
    if is_known(t):
        return t["value"]
    m = re.search(r"khai trong code: (.+)$", t.get("reason", ""))
    return m.group(1) if m else None


def fk_text(col):
    f = v(col.get("foreign_key"))
    return f"{f.get('table')}.{f.get('column')}" if isinstance(f, dict) else None


def gold_fk(c):
    f = c.get("foreign_key")
    if isinstance(f, dict):
        return f"{f.get('table')}.{f.get('column')}"
    return f if f else None


def norm_type(t):
    return re.sub(r"\s+", "", str(t or "")).lower().replace("sqlalchemy.", "").replace("sa.", "")


total = Counter()
for case in A.v1_cases()[:4]:
    snap, sources = snapshot.take(case["src"])
    tools = SourceTools(snap, sources)
    facts, limits, _ = static_facts(snap, sources, tools, snapshot.inventory(snap)["units"][0]["id"])
    tables = {v(f["attributes"]["name"]): f for f in facts if f["kind"] == "table" and v(f["attributes"].get("name"))}
    gold = {e["table"]: e for e in case["gold"].get("entities", [])}
    c = Counter()
    c["gold_tables"], c["got_tables"] = len(gold), len(tables)
    miss = sorted(set(gold) - set(tables))
    extra = sorted(set(tables) - set(gold))
    c["tables_tp"] = len(set(gold) & set(tables))
    notes = []
    for name in sorted(set(gold) & set(tables)):
        ge, f = gold[name], tables[name]
        ev = declared(f)
        if ev["path"] != ge["file"] or not ge["line_from"] <= ev["start_line"] <= ge.get("line_to", ge["line_from"]) + 2:
            notes.append(f"  vị trí {name}: gold {ge['file']}:{ge['line_from']} | got {ev['path']}:{ev['start_line']}")
            c["table_where_diff"] += 1
        cols = {v(x["name"]): x for x in (v(f["attributes"].get("columns")) or [])}
        gcols = {x["name"]: x for x in ge["columns"]}
        c["gold_cols"] += len(gcols)
        c["cols_tp"] += len(set(gcols) & set(cols))
        for n in sorted(set(gcols) - set(cols)):
            notes.append(f"  thiếu cột {name}.{n}")
        for n in sorted(set(cols) - set(gcols)):
            notes.append(f"  thừa cột {name}.{n}")
            c["cols_fp"] += 1
        for n in sorted(set(gcols) & set(cols)):
            g, x = gcols[n], cols[n]
            for key, got, want in (("pk", v(x.get("primary_key")), g.get("primary_key")),
                                   ("nullable", v(x.get("nullable")), g.get("nullable")),
                                   ("fk", fk_text(x), gold_fk(g))):
                c[f"{key}_checked"] += 1
                if got is None and want is not None and key != "fk":
                    c[f"{key}_unknown"] += 1
                    notes.append(f"  {key} chưa rõ {name}.{n}: gold {want}")
                elif (got or None) != (want or None):
                    c[f"{key}_wrong"] += 1
                    notes.append(f"  {key} lệch {name}.{n}: gold {want} | got {got}")
            c["type_checked"] += 1
            if norm_type(code_type(x)) != norm_type(g.get("type")):
                c["type_diff"] += 1
                notes.append(f"  kiểu khác {name}.{n}: gold {g.get('type')} | got {code_type(x)} (state={x.get('type', {}).get('state')})")
    total.update(c)
    print(f"== {case['name']}: bảng gold {c['gold_tables']}, đọc được {c['got_tables']}, khớp {c['tables_tp']}; "
          f"cột gold {c['gold_cols']}, khớp {c['cols_tp']}, thừa {c['cols_fp']}")
    if miss:
        print("  THIẾU BẢNG:", miss)
    if extra:
        print("  THỪA BẢNG:", extra)
    for n in notes[:40]:
        print(n)
    if len(notes) > 40:
        print(f"  ... còn {len(notes) - 40} dòng")
    print("  giới hạn tĩnh:", [x["code"] for x in limits])
print("TỔNG", dict(total))
