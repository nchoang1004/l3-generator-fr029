"""Write diagram.mmd, README.md and graph.json for one run."""
from __future__ import annotations

import json
from pathlib import Path

import verify

SHAPES = {"database": ('[("', '")]'), "cache": ('[("', '")]'), "queue": ('[/"', '"/]')}


def _label(text: str) -> str:
    return text.replace('"', "'").replace("\n", " ")


def mermaid(result: dict) -> str:
    comps = {c["id"]: c for c in result["components"]}
    lines = ["flowchart LR"]
    shared = [c for c in comps.values() if c["shared"]]
    for c in comps.values():
        if not c["shared"]:
            lines.append(f'  {c["id"]}["{_label(c["name"])}"]')
    if shared:
        lines.append('  subgraph shared["Dùng chung (không vẽ cạnh)"]')
        lines += [f'    {c["id"]}["{_label(c["name"])}"]' for c in shared]
        lines.append("  end")
    if result["externals"]:
        lines.append('  subgraph external["Hệ thống ngoài"]')
        for x in result["externals"]:
            left, right = SHAPES.get(x["kind"], ('(["', '"])'))
            lines.append(f'    {x["id"]}{left}{_label(x["name"])}{right}')
        lines.append("  end")
    for e in result["edges"]:
        lines.append(f'  {e["source"]} -->|"{_label(e["label"])}"| {e["target"]}')
    for x in result["externals"]:
        for e in x["edges"]:
            lines.append(f'  {e["source"]} -.->|"{_label(e["label"])}"| {x["id"]}')
    return "\n".join(lines) + "\n"


def _quote(q: dict | None) -> str:
    if not q:
        return "—"
    return f'`{q["file"]}:{q["line"]}` `{verify.norm(q["text"]).replace("|", "¦")[:90]}`'


def readme(result: dict, meta: dict) -> str:
    comps = {c["id"]: c for c in result["components"]}
    q, t = result["quotes"], meta["timing"]
    out = [f"# Sơ đồ component — {meta['repo']}", "",
           f"Trạng thái: **{meta['status']}**. Tên, vai trò, hệ thống ngoài là suy luận của AI; "
           "mỗi phát biểu có trích dẫn đã được code kiểm khớp nguyên văn với source. Cạnh do code vẽ.", "",
           f"- File trong phạm vi: {meta['files']}; component: {len(comps)}; cạnh vẽ: {len(result['edges'])}; "
           f"cạnh ẩn: {len(result['hidden_edges'])}; hệ thống ngoài: {len(result['externals'])}.",
           f"- Trích dẫn AI trả: {q['returned']}; hợp lệ: {q['valid']}; bị loại: {len(result['rejected'])}.",
           f"- Thời gian: tổng {t['total_s']} s = phân tích cục bộ {t['local_s']} s + AI {t['ai_s']} s "
           f"(model chạy {t['model_s']} s, chờ giới hạn tốc độ {t['waiting_s']} s).",
           f"- Token Groq: {meta['tokens']} ({meta['requests']} request mới, {meta['cached']} lấy từ cache).", "",
           "```mermaid", mermaid(result).rstrip(), "```", "", "## Component", "",
           "| ID | Tên | Vai trò | Trích dẫn | Số file |", "|---|---|---|---|---:|"]
    for c in comps.values():
        out.append(f"| {c['id']} | {c['name']}{' (dùng chung)' if c['shared'] else ''} | "
                   f"{c['role'] or '_chưa có trích dẫn hợp lệ_'} | {_quote(c['role_quote'])} | {len(c['files'])} |")
    out += ["", "## Cạnh được vẽ", "",
            "Cạnh do code vẽ theo quy tắc: mọi quan hệ import giữa hai khối, trừ khối dùng chung. "
            "Nhãn và trích dẫn do code lấy từ dòng dùng import; phía đích là nơi định nghĩa tên được dùng.", "",
            "| Từ | Tới | Nhãn | Trích dẫn phía nguồn | Phía đích |", "|---|---|---|---|---|"]
    for e in result["edges"]:
        target = ", ".join(f"`{p}:{n}`" for p, n in e["target_evidence"][:2]) or "—"
        out.append(f"| {comps[e['source']]['name']} | {comps[e['target']]['name']} | {e['label']} | "
                   f"{_quote(e['quote'])} | {target} |")
    for x in result["externals"]:
        for e in x["edges"]:
            out.append(f"| {comps[e['source']]['name']} | {x['name']} ({x['kind']}) | {e['label']} (AI) | "
                       f"{_quote(e['quote'])} | — |")
    if result["hidden_edges"]:
        out += ["", "## Cạnh có trong code nhưng không vẽ", "", "| Từ | Tới | Lý do | Trích dẫn |", "|---|---|---|---|"]
        for h in result["hidden_edges"]:
            out.append(f"| {comps[h['source']]['name']} | {comps[h['target']]['name']} | {h['reason']} | "
                       f"{_quote(h.get('quote'))} |")
    if result["rejected"]:
        out += ["", "## Bị loại vì trích dẫn không khớp", ""]
        out += [f"- {r['what']}: {r['reason']}" for r in result["rejected"]]
    out += ["", "## Giới hạn", "",
            "- Cạnh giữa component chỉ lấy từ import đã phân giải; lời gọi động, HTTP nội bộ, queue theo tên chưa thấy được.",
            "- Trích dẫn khớp chứng minh dòng code tồn tại, không chứng minh câu mô tả đúng nghĩa; cần người review.",
            *[f"- {i}" for i in meta["issues"]], ""]
    return "\n".join(out)


def write(out: Path, result: dict, meta: dict, snapshot: dict) -> None:
    out.mkdir(parents=True)
    (out / "diagram.mmd").write_text(mermaid(result), encoding="utf-8")
    (out / "README.md").write_text(readme(result, meta), encoding="utf-8")
    data = {"meta": meta, **result,
            "snapshot": {p: snapshot["files"][p]["sha256"] for p in snapshot["scope"]},
            "excluded": snapshot["excluded"]}
    (out / "graph.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
