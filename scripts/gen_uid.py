#!/usr/bin/env python3
"""Cấp ULID cho artifact chuẩn tắc còn thiếu `uid`.

    python scripts/gen_uid.py --check      # chỉ liệt kê file thiếu, không ghi
    python scripts/gen_uid.py              # điền uid vào các file đó

EXEC §A.4 ghi `uid` là "ULID — tool sinh, không gõ tay" nhưng repo chưa có tool
đó; các uid hiện có trong `.aide/` được sinh trong lúc soạn hồ sơ. Script này
lấp chỗ trống, dùng đúng bảng chữ mà `prd_package.py` đang kiểm:

    re.fullmatch(r"[0-7][0-9A-HJKMNP-TV-Z]{25}", uid)

tức Crockford Base32 26 ký tự, ký tự đầu ≤ 7 (48 bit timestamp không tràn).

Chỉ ghi vào file có `uid:` rỗng. File đã có uid thì không đụng, kể cả khi uid đó
sai định dạng — sửa một uid đã phát ra là đổi định danh của artifact, phải là
quyết định của người, không phải việc của script.

ULID sinh ở đây tự implement (48 bit thời gian + 80 bit ngẫu nhiên) để không
thêm phụ thuộc; hai script còn lại cũng chạy được khi máy không cài gì thêm.
"""

from __future__ import annotations

import argparse
import os
import re
import secrets
import sys
import time
from pathlib import Path

# Console Windows mặc định cp1252, không in được dấu tiếng Việt.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
AIDE = REPO / ".aide"

# Crockford Base32: bỏ I, L, O, U để không nhầm với 1, 0 và không tạo từ tục.
ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
ULID_RE = re.compile(r"[0-7][0-9A-HJKMNP-TV-Z]{25}")

# `generated/` là derived, không mang frontmatter chuẩn tắc (EXEC §A.2 luật 4).
SKIP_DIRS = {"generated"}


def encode(value: int, length: int) -> str:
    out = []
    for _ in range(length):
        out.append(ALPHABET[value & 31])
        value >>= 5
    return "".join(reversed(out))


def new_ulid() -> str:
    """48 bit millisecond + 80 bit ngẫu nhiên, theo spec ULID."""
    return encode(int(time.time() * 1000), 10) + encode(secrets.randbits(80), 16)


def rel(path: Path) -> str:
    return str(path.relative_to(REPO)).replace("\\", "/")


def uid_line(text: str) -> re.Match | None:
    """Tìm dòng `uid:` trong frontmatter, trả về match hoặc None.

    Chỉ nhìn phần giữa hai dấu `---` đầu file; `uid:` xuất hiện trong thân bài
    (ví dụ khi tài liệu trích dẫn mẫu frontmatter) không được tính.
    """
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return re.search(r"^uid:[ \t]*(.*)$", text[: end + 1], re.M)


def collect() -> tuple[list[Path], list[tuple[Path, str]], list[Path]]:
    """Duyệt `.aide/`, chia file thành ba nhóm."""
    missing: list[Path] = []
    filled: list[tuple[Path, str]] = []
    malformed: list[Path] = []
    for path in sorted(AIDE.rglob("*.md")):
        if SKIP_DIRS & set(path.relative_to(AIDE).parts):
            continue
        m = uid_line(path.read_text(encoding="utf-8"))
        if m is None:
            continue
        value = m.group(1).strip().strip('"').strip("'")
        if not value:
            missing.append(path)
        elif ULID_RE.fullmatch(value):
            filled.append((path, value))
        else:
            malformed.append(path)
    return missing, filled, malformed


def write_uid(path: Path, uid: str) -> None:
    text = path.read_text(encoding="utf-8")
    m = uid_line(text)
    if m is None:
        raise RuntimeError(f"{rel(path)}: mất dòng uid giữa chừng")
    patched = text[: m.start()] + f'uid: "{uid}"' + text[m.end() :]
    # newline="" giữ nguyên line ending sẵn có của file, không đổi CRLF↔LF.
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(patched)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="chỉ báo, không ghi")
    args = ap.parse_args(argv)

    if not AIDE.is_dir():
        print(f"không có thư mục {rel(AIDE)}")
        return 1

    missing, filled, malformed = collect()

    seen: dict[str, Path] = {}
    duplicates: list[str] = []
    for path, uid in filled:
        if uid in seen:
            duplicates.append(f"{uid} ở {rel(seen[uid])} và {rel(path)}")
        seen[uid] = path

    print(f"Artifact có dòng uid: {len(missing) + len(filled) + len(malformed)}")
    print(f"  đã có uid hợp lệ: {len(filled)}")
    print(f"  thiếu uid:        {len(missing)}")
    print(f"  uid sai định dạng:{len(malformed)}")
    print()

    for path in malformed:
        print(f"  SAI ĐỊNH DẠNG (không tự sửa): {rel(path)}")
    for line in duplicates:
        print(f"  TRÙNG uid: {line}")

    if not missing:
        print("Không file nào thiếu uid.")
        return 1 if (malformed or duplicates) else 0

    if args.check:
        print("Thiếu uid:")
        for path in missing:
            print(f"  - {rel(path)}")
        print(f"\nChạy lại không có --check để điền {len(missing)} uid.")
        return 1

    for path in missing:
        uid = new_ulid()
        while uid in seen:  # 80 bit ngẫu nhiên nên thực tế không vào vòng này
            uid = new_ulid()
        seen[uid] = path
        write_uid(path, uid)
        print(f"  {uid}  {rel(path)}")

    print(f"\nĐã điền {len(missing)} uid.")
    return 1 if (malformed or duplicates) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
