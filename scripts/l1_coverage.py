#!/usr/bin/env python3
"""Kiểm luật coverage #2 — mọi FR có ít nhất một CAP `covers` về nó.

    py -3.12 scripts/l1_coverage.py

Đọc `.aide/requirements/fr/` và `.aide/architecture/l1/`, đối chiếu hai chiều
rồi in bảng. Thoát 0 khi không lệch, 1 khi có lệch.

Bốn loại lệch được báo:

- FR không có CAP nào `covers` — chính là luật coverage #2 ở EXEC §B.7.
- CAP `covers` tới một FR key không tồn tại.
- CAP không `covers` FR nào — năng lực rỗng, nhiều khả năng viết sót.
- `verified_against` của CAP lệch revision so với file FR hiện tại.

Script này đọc frontmatter cục bộ trong `.aide/`, không đọc metadata graph tập
trung. Nó không phải công cụ `aide` chính thức, và không kiểm L2 hay CMP.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Console Windows mặc định cp1252, không in được dấu tiếng Việt ở phần kết luận.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
AIDE = REPO / ".aide"
FR_DIR = AIDE / "requirements" / "fr"
L1_DIR = AIDE / "architecture" / "l1"


def frontmatter(raw: bytes) -> dict[str, str]:
    """Lấy các trường vô hướng ở frontmatter.

    Cùng cách đọc với `prd_package.py`: regex thay cho thư viện YAML, để script
    chạy được khi máy không cài PyYAML. `relations` và `verified_against` là
    JSON một dòng nên người gọi tự `json.loads` phần cần.
    """
    text = raw.decode("utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict[str, str] = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"')
    return out


def load_json_field(front: dict[str, str], name: str, where: str):
    raw = front.get(name, "").strip()
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"  LỖI: {where} có `{name}` không đọc được thành JSON")
        return None


def rel(path: Path) -> str:
    return str(path.relative_to(REPO)).replace("\\", "/")


def main() -> int:
    if not FR_DIR.is_dir():
        print(f"không có thư mục {rel(FR_DIR)}")
        return 1
    if not L1_DIR.is_dir():
        print(f"không có thư mục {rel(L1_DIR)} — L1 chưa được lập")
        return 1

    fr_revision: dict[str, int] = {}
    for path in sorted(FR_DIR.glob("*.md")):
        front = frontmatter(path.read_bytes())
        key = front.get("key", "")
        if not key:
            print(f"  LỖI: {rel(path)} không có `key`")
            return 1
        fr_revision[key] = int(front.get("revision", 0))

    covered_by: dict[str, list[str]] = {key: [] for key in fr_revision}
    issues: list[str] = []

    for path in sorted(L1_DIR.glob("CAP-*.md")):
        front = frontmatter(path.read_bytes())
        cap = front.get("key", rel(path))
        relations = load_json_field(front, "relations", rel(path)) or {}
        covers = relations.get("covers", [])
        if not covers:
            issues.append(f"{cap} không `covers` FR nào")
        verified = {
            entry.get("key"): entry.get("revision")
            for entry in (load_json_field(front, "verified_against", rel(path)) or [])
        }
        for fr in covers:
            if fr not in fr_revision:
                issues.append(f"{cap} `covers` {fr} nhưng không có file FR đó")
                continue
            covered_by[fr].append(cap)
            if fr in verified and verified[fr] != fr_revision[fr]:
                issues.append(
                    f"{cap} khai {fr} revision {verified[fr]}, "
                    f"file hiện tại revision {fr_revision[fr]}"
                )

    print(f"FR: {len(fr_revision)}   CAP: {len(list(L1_DIR.glob('CAP-*.md')))}")
    print()
    print("FR key            rev  CAP covers")
    print("-" * 58)
    for fr in sorted(fr_revision):
        caps = ", ".join(covered_by[fr]) or "— KHÔNG CÓ —"
        print(f"{fr}  {fr_revision[fr]:>3}  {caps}")
        if not covered_by[fr]:
            issues.append(f"{fr} không có CAP nào `covers` (luật coverage #2)")

    print()
    if issues:
        print(f"LỆCH — {len(issues)} vấn đề:")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    print("XANH — mọi FR có ≥1 CAP `covers`, revision khớp.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
