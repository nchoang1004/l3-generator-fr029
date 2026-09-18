#!/usr/bin/env python3
"""Tính impact.yaml từ quan hệ khai trong frontmatter của `.aide/`.

    py -3.12 scripts/impact.py --baseline BL-r12.yaml

Quy trình (EXEC §B.3) nói `impact.yaml` sinh từ **metadata graph tập trung**.
Repo này không có graph đó. Script dựng graph cục bộ từ chính `relations` trong
frontmatter — đủ để tính `touches` và `stale_artifacts` thật, nhưng không thay
được graph tổ chức.

Giới hạn, đã khai vào `confidence` và `skipped_with_reason` của file sinh ra:

- Không thấy consumer ngoài repo, nên `external_consumers` luôn rỗng ở đây.
- Chỉ thấy artifact **đang tồn tại**. Yêu cầu bị bỏ sót hoàn toàn thì không có
  node nào để phát hiện — việc đó phải đọc đề bài bằng mắt.
- `tier` và `flow` đọc từ `change-set.yaml`; script không tự quyết.

Script không ghi đè file đã có nếu nội dung khác, trừ khi truyền --force.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AIDE = REPO / ".aide"
CHANGE_SETS = AIDE / "lifecycle" / "change-sets"

# Quan hệ đi từ artifact này tới artifact khác. Dùng để lan truyền stale.
OUTGOING = ("satisfies", "constrained_by", "measured_by", "covers", "blocked_by")


def frontmatter(raw: bytes) -> dict:
    """Đọc frontmatter. Giá trị JSON một dòng (relations, ownership) được parse."""
    text = raw.decode("utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val.startswith("{") or val.startswith("["):
            try:
                out[key] = json.loads(val)
                continue
            except json.JSONDecodeError:
                pass
        out[key] = val.strip('"')
    return out


def load_artifacts() -> dict[str, dict]:
    """Nạp mọi artifact chuẩn tắc có `key` trong `.aide/`."""
    arts: dict[str, dict] = {}
    for path in AIDE.rglob("*.md"):
        if "generated" in path.parts:
            continue
        fm = frontmatter(path.read_bytes())
        key = fm.get("key")
        if key:
            fm["_path"] = str(path.relative_to(REPO)).replace("\\", "/")
            arts[key] = fm
    return arts


def parse_change_set(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    out: dict = {}
    for line in text.splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"')
    return out


def baseline_keys(path: Path) -> dict[str, int]:
    text = path.read_text(encoding="utf-8")
    return {
        m.group(1): int(m.group(2))
        for m in re.finditer(r"- key: (\S+)\n  revision: (\d+)", text)
    }


def reverse_edges(arts: dict[str, dict]) -> dict[str, set[str]]:
    """Ai trỏ tới mình. Một artifact đổi thì những người trỏ tới nó thành stale."""
    back: dict[str, set[str]] = {k: set() for k in arts}
    for key, fm in arts.items():
        rel = fm.get("relations") or {}
        if not isinstance(rel, dict):
            continue
        for name in OUTGOING:
            for target in rel.get(name, []) or []:
                if target in back:
                    back[target].add(key)
    return back


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--force", action="store_true", help="ghi đè impact.yaml đã có")
    args = ap.parse_args(argv)

    dirs = [p for p in CHANGE_SETS.iterdir() if p.is_dir()]
    if len(dirs) != 1:
        print(f"LỖI: cần đúng một Change Set, thấy {len(dirs)}", file=sys.stderr)
        return 1
    chg_dir = dirs[0]
    chg = parse_change_set(chg_dir / "change-set.yaml")

    cr_key = chg.get("change_request", "")
    cr_path = AIDE / "evidence" / "requests" / f"{cr_key}.yaml"
    if not cr_path.exists():
        print(f"LỖI: không có CR {cr_key} — §B.3 bắt buộc CR tồn tại", file=sys.stderr)
        return 1

    arts = load_artifacts()
    bl = baseline_keys(chg_dir / "baseline" / args.baseline)
    back = reverse_edges(arts)

    # touches: artifact trong baseline candidate — flow new-system nên toàn bộ là mới.
    touches = sorted(k for k in bl if k in arts)

    # stale: artifact NGOÀI baseline nhưng trỏ tới thứ trong baseline.
    stale = sorted({s for k in bl for s in back.get(k, ()) if s not in bl})

    teams = sorted(
        {
            (fm.get("ownership") or {}).get("accountable_team")
            for k, fm in arts.items()
            if k in bl and isinstance(fm.get("ownership"), dict)
        }
        - {None}
    )

    # risk_signals suy từ NFR có mặt trong baseline, không gõ tay.
    risk = {
        "source_code_ingestion": any(k.startswith("NFR-L3GEN-SEC") for k in bl),
        "remote_fetch": any(k == "FR-L3GEN-016" for k in bl),
        "third_party_ai": any(k.startswith("NFR-L3GEN-AI") for k in bl),
        "user_data_retention": any(k.startswith("NFR-L3GEN-PRIV") for k in bl),
        "pii": None,
        "financial": None,
    }

    blocked = sorted(
        k
        for k in bl
        if isinstance(arts.get(k, {}).get("relations"), dict)
        and (arts[k]["relations"].get("blocked_by") or [])
    )

    lines = [
        "# Sinh bằng scripts/impact.py — không sửa tay.",
        "# Đọc quan hệ khai trong frontmatter của .aide/, KHÔNG phải metadata graph",
        "# tập trung mà EXEC §B.3 mô tả. Xem confidence và skipped_with_reason.",
        "",
        f"change_request: {cr_key}",
        f"flow: {chg.get('flow', 'unknown')}",
        f"tier: {chg.get('tier', 'null')}",
        f"baseline_analyzed: {args.baseline}",
        "",
        "touches:",
        *[f"  - {k}" for k in touches],
        "",
        "stale_artifacts: []"
        if not stale
        else "stale_artifacts:\n" + "\n".join(f"  - {k}" for k in stale),
        "",
        "affected_teams:",
        *[f"  - {t}" for t in teams],
        "",
        "external_consumers: []",
        "",
        "risk_signals:",
        *[f"  {k}: {('null' if v is None else str(v).lower())}" for k, v in risk.items()],
        "",
        "path_signals:",
        '  - ".aide/requirements/**"',
        '  - ".aide/product/prd/**"',
        '  - "src/l3gen/**"',
        '  - "tests/**"',
        "",
        "blocked_by_open_questions:",
        *[
            f"  - {{ artifact: {k}, blocked_by: {json.dumps(arts[k]['relations']['blocked_by'])} }}"
            for k in blocked
        ],
        "",
        "skipped_with_reason:",
        '  - { area: "external_consumers", reason: "Không có metadata graph tập trung nên'
        " không thấy hệ thống ngoài repo. Chưa kiểm chứng consumer bên"
        ' ngoài; danh sách rỗng không chứng minh không có consumer." }',
        '  - { area: "architecture-and-contracts", reason: "Chưa có artifact L1/L2/L3 nào'
        " hoàn chỉnh được xác nhận; đã có ADR draft. Chưa đủ graph để kết luận toàn bộ"
        ' tác động tới thiết kế." }',
        '  - { area: "code-traceability", reason: "Chưa thực hiện quét source/test trong script này cho'
        " mã FR/AC/NFR; không suy được thay đổi yêu cầu chạm"
        ' file code nào." }',
        '  - { area: "missing-requirements", reason: "Script chỉ thấy artifact đang tồn tại;'
        " yêu cầu bị bỏ sót hoàn toàn thì không có node để phát hiện. Hai chỗ hở đã tìm được"
        " (entry point, thư viện bên ngoài) là do đọc đề bài mục 3.6 bằng mắt, không do"
        ' script. Việc rà đủ vẫn thuộc về người." }',
        "",
        "confidence:",
        "  graph_coverage: local-frontmatter-only",
        "  level: low",
        "  basis: >-",
        f"    Tính từ {len(arts)} artifact có frontmatter trong .aide/."
        " Quan hệ đọc từ trường relations, không qua graph tập trung.",
        "  not_established: >-",
        "    Tính đủ của bộ yêu cầu so với đề bài; ảnh hưởng tới hệ thống ngoài;"
        " ảnh hưởng tới code.",
        "",
        "review_note: >-",
        "  Bản này không thay việc mentor rà soát phạm vi. Nó nói thay đổi chạm những artifact",
        "  nào trong repo, không nói bộ yêu cầu đã đủ hay chưa.",
    ]

    target = chg_dir / "impact.yaml"
    content = "\n".join(lines) + "\n"

    # Tự kiểm cú pháp trước khi ghi. Một lần thiếu dấu nháy đã lọt qua mắt
    # nhưng làm cả file không parse được — CI sẽ reject, và người đọc không
    # nhìn ra. Có PyYAML thì bắt ngay ở đây; không có thì báo là chưa kiểm.
    try:
        import yaml  # noqa: PLC0415 — phụ thuộc tùy chọn, chỉ dùng để tự kiểm

        parsed = yaml.safe_load(content)
        for field in ("tier", "flow", "confidence", "skipped_with_reason"):
            if not parsed.get(field):
                print(f"LỖI: thiếu `{field}` — §B.3 yêu cầu có đủ bốn trường", file=sys.stderr)
                return 1
        syntax_note = "YAML parse được, đủ bốn trường bắt buộc"
    except ImportError:
        syntax_note = "CHƯA kiểm cú pháp (không có PyYAML)"
    except yaml.YAMLError as exc:  # type: ignore[name-defined]
        print(f"LỖI: YAML sinh ra không parse được: {exc}", file=sys.stderr)
        return 1
    if target.exists() and not args.force:
        if target.read_text(encoding="utf-8") == content:
            print("impact.yaml đã đúng, không đổi.")
            return 0
        print(f"LỖI: {target.name} đã tồn tại và khác nội dung. Dùng --force.", file=sys.stderr)
        return 1
    target.write_text(content, encoding="utf-8", newline="\n")

    print(f"Đã ghi {target.relative_to(REPO)}")
    print(f"  {syntax_note}")
    print(f"  touches: {len(touches)} · stale: {len(stale)} · teams: {len(teams)}")
    print(f"  FR bị OQ chặn: {len(blocked)}")
    print(f"  tier: {chg.get('tier')} · flow: {chg.get('flow')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
