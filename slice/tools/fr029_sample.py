"""Pick the same review sample from a run for every grader: some routes, some files with roles, all HTTP calls.

    python slice/tools/fr029_sample.py RESULT_JSON [--routes 10] [--files 15] [--seed 29]

Prints a Markdown list. The choice depends only on the result and the seed, so each grader checks the same items.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("result", type=Path)
    p.add_argument("--routes", type=int, default=10)
    p.add_argument("--files", type=int, default=15)
    p.add_argument("--seed", type=int, default=29)
    a = p.parse_args(argv)
    r = json.loads(a.result.read_text(encoding="utf-8"))
    rnd = random.Random(a.seed)
    routes = sorted((f for f in r["facts"] if f["kind"] == "route"), key=lambda f: f["id"])
    roles = sorted((f for f in r["facts"] if f["kind"] == "file_role"), key=lambda f: f["attributes"]["file"]["value"])
    calls = [f for f in r["facts"] if f["kind"] == "http_call"]
    pick_r = rnd.sample(routes, min(a.routes, len(routes)))
    pick_f = rnd.sample(roles, min(a.files, len(roles)))
    out = [f"Route cần kiểm ({len(pick_r)}/{len(routes)}):"]
    for f in sorted(pick_r, key=lambda f: f["evidence"][0]["path"]):
        x = f["attributes"]
        path = x["path"]["value"] if x["path"]["state"] == "known" else "(path unknown)"
        out.append(f"- {x['method']['value']} {path} — handler {x['handler']['value']} (fact {f['id'][:13]})")
    out.append(f"\nFile cần kiểm vai trò ({len(pick_f)}/{len(roles)}):")
    out += [f"- {f['attributes']['file']['value']}" for f in pick_f]
    out.append(f"\nLời gọi HTTP ra ngoài (tất cả {len(calls)}):")
    out += [f"- {f['evidence'][0]['path']}:{f['evidence'][0]['start_line']}" for f in calls] or ["- (không có)"]
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
