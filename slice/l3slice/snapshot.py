"""CMP-002/003 subset: snapshot of a local directory or a ZIP archive, and a one-unit inventory.

Only `.py` files and Python manifests (`pyproject.toml`, `requirements*.txt`) are read. Other files are listed as
excluded with a reason. A ZIP is checked entry by entry and never written to disk (API-002 §2).
GitHub fetch and multi-unit root detection are not here: API-002 §1 and API-003 §1 require a review before code.
"""
from __future__ import annotations

import io
import re
import stat
import unicodedata
import zipfile
from pathlib import Path

from .common import SCHEMA_VERSION, compact, sha

MANIFESTS = re.compile(r"(^|/)(pyproject\.toml|requirements[^/]*\.txt)$")
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules"}
ZIP_MAX_COMPRESSED, ZIP_MAX_UNCOMPRESSED, ZIP_MAX_FILES = 100_000_000, 500_000_000, 50_000
WINDOWS_RESERVED = re.compile(r"^(con|prn|aux|nul|com[0-9]|lpt[0-9])(\..*)?$", re.I)


class IntakeError(ValueError):
    """API-002 SnapshotError for `create_snapshot`."""

    def __init__(self, code: str, message: str, action: str, run_id: str = "run_local"):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.payload = {"code": code, "message": message, "action": action, "retryable": False,
                        "operation": "create_snapshot", "run_id": run_id, "snapshot_id": None, "file_id": None}


def _wanted(rel: str) -> bool:
    return rel.endswith(".py") or bool(MANIFESTS.search(rel))


SKIP_REASON = "Thư mục công cụ hoặc môi trường (.git, .venv, venv, node_modules, __pycache__), không đọc"


def _skipped(rel: str) -> str | None:
    """Prefix of the first tool/environment directory in the path; same rule for local and ZIP (API-002 §2)."""
    parts = rel.split("/")
    for i, part in enumerate(parts):
        if part in SKIP_DIRS:
            return "/".join(parts[:i + 1])
    return None


def _skip_entry(excluded: list, prefix: str):
    if not any(e["path"] == prefix for e in excluded):
        excluded.append({"path": prefix, "reason": SKIP_REASON})


def take(root: Path) -> tuple[dict, dict[str, bytes]]:
    excluded, sources = [], {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        prefix = _skipped(rel)
        if prefix is not None:
            _skip_entry(excluded, prefix)
            continue
        if path.is_symlink():
            excluded.append({"path": rel, "reason": "Symlink không được đi theo"})
            continue
        if not path.is_file():
            continue
        if not _wanted(rel):
            excluded.append({"path": rel, "reason": "Chỉ đọc file .py và manifest Python"})
            continue
        sources[rel] = path.read_bytes()
    return _snapshot(sources, excluded), sources


def _check_name(name: str, run_id: str) -> str:
    """Entry path rules of API-002 §2. Returns the path without a trailing `/`."""
    if "\\" in name or "\0" in name or ":" in name:
        raise IntakeError("PATH_ESCAPE", "Tên entry có backslash, NUL hoặc dấu hai chấm",
                          "Đóng gói lại ZIP bằng đường dẫn POSIX", run_id)
    rel = name[:-1] if name.endswith("/") else name
    segments = rel.split("/")
    if not rel or rel.startswith("/") or any(seg in ("", ".", "..") for seg in segments):
        raise IntakeError("PATH_ESCAPE", "Entry có đường dẫn tuyệt đối, rỗng, '.' hoặc '..'",
                          "Bỏ entry thoát khỏi thư mục gốc", run_id)
    if any(seg != seg.rstrip(". ") or WINDOWS_RESERVED.match(seg) for seg in segments):
        raise IntakeError("PATH_COLLISION", "Tên kết thúc bằng dấu chấm/khoảng trắng hoặc là tên dành riêng của Windows",
                          "Đổi tên file rồi đóng gói lại", run_id)
    return rel


def take_zip(archive: Path | bytes, run_id: str = "run_local", strip_wrapper: bool = False) -> tuple[dict, dict[str, bytes]]:
    """The whole archive is refused on the first bad entry; nothing is written to disk.
    `strip_wrapper`: remove the single top folder that the GitHub zipball adds (API-002 §2), nothing else."""
    size = len(archive) if isinstance(archive, bytes) else archive.stat().st_size
    if size > ZIP_MAX_COMPRESSED:
        raise IntakeError("INTAKE_LIMIT", "ZIP vượt 100.000.000 byte nén", "Giảm kích thước ZIP", run_id)
    try:
        zf = zipfile.ZipFile(io.BytesIO(archive) if isinstance(archive, bytes) else archive)
    except (zipfile.BadZipFile, OSError):
        raise IntakeError("ZIP_INVALID", "File không phải ZIP hợp lệ", "Tạo lại file ZIP", run_id) from None
    sources, excluded, seen, total, count = {}, [], set(), 0, 0
    wrapper = None
    if strip_wrapper:
        tops = {_check_name(i.orig_filename, run_id).split("/", 1)[0] for i in zf.infolist()}
        if len(tops) != 1:
            raise IntakeError("ZIP_INVALID", "Zipball không có đúng một thư mục bọc ngoài", "Tạo run mới", run_id)
        wrapper = tops.pop() + "/"
    with zf:
        for info in zf.infolist():
            rel = _check_name(info.orig_filename, run_id)  # zipfile turns "\\" into "/" on Windows
            if wrapper is not None:
                if rel + "/" == wrapper:
                    continue
                rel = rel[len(wrapper):]
            mode = info.external_attr >> 16
            if stat.S_ISLNK(mode):
                raise IntakeError("LINK_NOT_ALLOWED", "ZIP chứa liên kết", "Bỏ symlink khỏi ZIP", run_id)
            if info.flag_bits & 0x1:
                raise IntakeError("ZIP_INVALID", "ZIP có entry mã hóa", "Tạo ZIP không mật khẩu", run_id)
            if stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR):  # 0: tool wrote permissions only
                raise IntakeError("ZIP_INVALID", "Entry không phải file thường hoặc thư mục", "Bỏ file đặc biệt", run_id)
            key = unicodedata.normalize("NFC", rel).casefold()
            if key in seen:
                raise IntakeError("PATH_COLLISION", "Hai entry trùng tên khi bỏ qua hoa/thường hoặc dạng Unicode",
                                  "Đổi tên một trong hai file", run_id)
            seen.add(key)
            prefix = _skipped(rel)
            if prefix is not None:
                _skip_entry(excluded, prefix)
            if info.is_dir():
                continue
            count += 1
            if count > ZIP_MAX_FILES:
                raise IntakeError("INTAKE_LIMIT", "ZIP có hơn 50.000 file", "Giảm số file", run_id)
            data, keep = bytearray(), prefix is None and _wanted(rel)  # skipped files still count toward limits
            try:
                with zf.open(info) as fh:
                    while chunk := fh.read(1 << 20):  # count real bytes, not the size written in the header
                        total += len(chunk)
                        if total > ZIP_MAX_UNCOMPRESSED:
                            raise IntakeError("INTAKE_LIMIT", "Dữ liệu giải nén vượt 500.000.000 byte",
                                              "Giảm kích thước ZIP", run_id)
                        if keep:
                            data += chunk
            except (zipfile.BadZipFile, RuntimeError, NotImplementedError, EOFError):
                raise IntakeError("ZIP_INVALID", "Không giải nén được một entry", "Tạo lại file ZIP", run_id) from None
            if keep:
                sources[rel] = bytes(data)
            elif prefix is None:
                excluded.append({"path": rel, "reason": "Chỉ đọc file .py và manifest Python"})
    return _snapshot(sources, excluded), sources


def _snapshot(sources: dict[str, bytes], excluded: list) -> dict:
    files = [{"file_id": "file:" + sha(rel.encode()), "path": rel, "sha256": sha(raw), "byte_size": len(raw),
              "encoding": "utf-8"} for rel, raw in sorted(sources.items())]
    manifest = [[f["path"], f["sha256"], f["byte_size"]] for f in files]
    snapshot_id = "snap:" + sha(compact(manifest).encode())
    return {"schema_version": SCHEMA_VERSION, "snapshot_id": snapshot_id, "files": files,
            "excluded": sorted(excluded, key=lambda e: e["path"])}


def inventory(snapshot: dict) -> dict:
    snap = snapshot["snapshot_id"]
    files = snapshot["files"]
    units = []
    if files:
        units.append({"id": "unit:" + sha((snap + "\n.").encode()), "root_path": ".", "language": "Python",
                      "framework": "FastAPI/SQLAlchemy", "support": "partial",
                      "file_ids": [f["file_id"] for f in files], "flat": False})
    return {"schema_version": SCHEMA_VERSION, "snapshot_id": snap, "support_matrix_version": "slice-v1",
            "grouping_policy_version": "fixture-membership-v1", "outcome": "ready" if files else "empty",
            "units": units, "excluded": list(snapshot["excluded"]), "limitations": [
                {"code": "SLICE_SCOPE", "message": "Lát cắt đầu chỉ nhận route FastAPI và bảng SQLAlchemy Column",
                 "stage": "inventory", "affected_ids": [u["id"] for u in units]}]}
