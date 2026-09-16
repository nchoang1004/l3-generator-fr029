"""Kiểm kê repository theo file rồi nhóm phần có thể phân tích theo ngôn ngữ.

V2 không dùng folder hoặc manifest để quyết định file nào được parse. Manifest chỉ
là bằng chứng nhận diện framework; application/service boundary được dựng sau graph.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from l3gen.models.inventory import FileInventory, SourceFileRecord
from l3gen.models.stack import DetectedStack, ServiceUnit

MANIFESTS: dict[str, str] = {
    "requirements.txt": "python",
    "pyproject.toml": "python",
    "Pipfile": "python",
    "setup.py": "python",
    "pom.xml": "java",
    "build.gradle": "java",
    "build.gradle.kts": "java",
    "package.json": "javascript",
    "go.mod": "go",
}

EXTENSION_LANGUAGE = {
    ".py": "python",
    ".pyi": "python",
    ".java": "java",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "javascript",
    ".tsx": "javascript",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".php": "php",
    ".cs": "csharp",
    ".c": "c",
    ".h": "c",
    ".cc": "cpp",
    ".cpp": "cpp",
    ".cxx": "cpp",
    ".hpp": "cpp",
    ".swift": "swift",
    ".scala": "scala",
}

SUPPORTED_LANGUAGES = frozenset({"python"})
MAX_SOURCE_BYTES = 2 * 1024 * 1024
MAX_ANALYZED_FILES = 20_000
MAX_ANALYZED_BYTES = 128 * 1024 * 1024

FRAMEWORK_MANIFEST_MARKERS = {
    "fastapi": ("fastapi",),
    "flask": ("flask",),
    "django": ("django",),
}

FRAMEWORK_IMPORT_MARKERS = {
    "fastapi": ("from fastapi", "import fastapi", "FastAPI(", "APIRouter("),
    "flask": ("from flask", "import flask", "Flask(", "Blueprint("),
    "django": ("from django", "import django"),
}

ORM_MARKERS = {"sqlalchemy": ("sqlalchemy", "sqlmodel")}


@dataclass
class Unit:
    """Nhóm file cùng ngôn ngữ; không phải service/application boundary."""

    root: Path
    name: str
    language: str
    files: list[Path] = field(default_factory=list)
    manifests: list[Path] = field(default_factory=list)
    inventory_records: list[SourceFileRecord] = field(default_factory=list)
    rel_root: str = ""

    @property
    def manifest(self) -> str | None:
        if not self.manifests:
            return None
        return self.manifests[0].relative_to(self.root).as_posix()


def _is_excluded(path: Path, root: Path, excludes: set[str]) -> str | None:
    for part in path.relative_to(root).parts[:-1]:
        if part in excludes:
            return part
    return None


def _digest(path: Path) -> str | None:
    hasher = hashlib.sha256()
    try:
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(64 * 1024), b""):
                hasher.update(chunk)
    except OSError:
        return None
    return f"sha256:{hasher.hexdigest()}"


def inventory_repository(
    root: Path,
    excludes: tuple[str, ...],
    max_source_bytes: int = MAX_SOURCE_BYTES,
    max_analyzed_files: int = MAX_ANALYZED_FILES,
    max_analyzed_bytes: int = MAX_ANALYZED_BYTES,
) -> tuple[FileInventory, list[Unit]]:
    """Duyệt mỗi path một lần và tạo sổ cái source độc lập với cấu trúc folder."""
    excluded_names = set(excludes)
    records: list[SourceFileRecord] = []
    manifests_by_language: dict[str, list[Path]] = {}
    analyzed_count = analyzed_bytes = 0

    paths = sorted(path for path in root.rglob("*") if path.is_file())
    for path in paths:
        manifest_language = MANIFESTS.get(path.name)
        if manifest_language and _is_excluded(path, root, excluded_names) is None:
            manifests_by_language.setdefault(manifest_language, []).append(path)

        language = EXTENSION_LANGUAGE.get(path.suffix.lower())
        if language is None:
            continue

        rel_path = path.relative_to(root).as_posix()
        try:
            size = path.stat().st_size
        except OSError:
            size = 0
        excluded_by = _is_excluded(path, root, excluded_names)
        digest = None

        if path.is_symlink():
            status = "excluded"
            reason = "symbolic link không được theo ra ngoài cây source"
        elif excluded_by is not None:
            status = "excluded"
            reason = f"nằm trong thư mục bị loại '{excluded_by}'"
        elif size > max_source_bytes:
            status = "oversized"
            reason = f"kích thước {size} byte vượt giới hạn {max_source_bytes} byte"
        elif language not in SUPPORTED_LANGUAGES:
            status = "unsupported_language"
            reason = f"frontend {language} chưa được triển khai"
        else:
            status = "discovered"
            reason = None
            if analyzed_count >= max_analyzed_files or analyzed_bytes + size > max_analyzed_bytes:
                status = "budget_exceeded"
                reason = f"vượt ngân sách parse {max_analyzed_files} file / {max_analyzed_bytes} byte"
            else:
                analyzed_count += 1
                analyzed_bytes += size
        if status not in ("excluded", "oversized", "budget_exceeded"):
            digest = _digest(path)
            if digest is None:
                status = "parse_error"
                reason = "không đọc được file để lập digest"

        records.append(
            SourceFileRecord(
                path=rel_path,
                language=language,
                size_bytes=size,
                digest=digest,
                status=status,
                reason=reason,
            )
        )

    units: list[Unit] = []
    for language in sorted({record.language for record in records}):
        language_records = [record for record in records if record.language == language]
        analyzable = [
            root / record.path for record in language_records if record.status == "discovered"
        ]
        units.append(
            Unit(
                root=root,
                name=language,
                language=language,
                files=analyzable,
                manifests=manifests_by_language.get(language, []),
                inventory_records=language_records,
            )
        )

    return FileInventory(files=records), units


def find_units(root: Path, excludes: tuple[str, ...]) -> list[Unit]:
    """API tương thích: trả các nhóm ngôn ngữ thay vì nhóm theo manifest."""
    _, units = inventory_repository(root, excludes)
    return units


def detect_stack(unit: Unit) -> ServiceUnit:
    """Nhận diện framework như metadata; không dùng nó để lọc source."""
    manifest_text = _read_manifests(unit)
    source_text = _read_sources(unit)
    frameworks: list[str] = []
    in_manifest: list[str] = []
    in_source: list[str] = []

    for framework, markers in FRAMEWORK_IMPORT_MARKERS.items():
        if unit.language != "python":
            continue
        from_manifest = any(
            marker in manifest_text
            for marker in FRAMEWORK_MANIFEST_MARKERS.get(framework, ())
        )
        from_source = any(marker in source_text for marker in markers)
        if from_manifest or from_source:
            frameworks.append(framework)
            if from_manifest:
                in_manifest.append(framework)
            if from_source:
                in_source.append(framework)

    orm = next(
        (
            name
            for name, markers in ORM_MARKERS.items()
            if any(marker in manifest_text or marker in source_text for marker in markers)
        ),
        None,
    )
    completeness, reason = _evidence_note(unit, frameworks, in_manifest, in_source)
    analyzed, skip_reason = _support_decision(unit)
    return ServiceUnit(
        name=unit.name,
        root_path="",
        manifest_file=unit.manifest,
        language=unit.language,
        frameworks=sorted(frameworks),
        orm=orm,
        confidence="exact",
        completeness=completeness,
        detection_reason=reason,
        file_count=len(unit.inventory_records),
        analyzed=analyzed,
        skip_reason=skip_reason,
    )


def _evidence_note(unit, frameworks, in_manifest, in_source) -> tuple[str, str]:
    if not frameworks:
        return "partial", f"nhận diện {unit.language} theo phần mở rộng; chưa thấy framework"
    if not unit.manifests:
        return "partial", f"thấy {', '.join(in_source)} trong source; chưa thấy manifest"
    only_manifest = [framework for framework in frameworks if framework not in in_source]
    if only_manifest:
        return "partial", f"{', '.join(only_manifest)} có trong manifest nhưng chưa thấy dùng"
    return "full", f"{', '.join(sorted(frameworks))} có trong manifest và source"


def _support_decision(unit: Unit) -> tuple[bool, str | None]:
    if unit.language not in SUPPORTED_LANGUAGES:
        return False, f"frontend {unit.language} chưa được hỗ trợ"
    if not unit.files:
        return False, "không còn file có thể parse sau exclude và giới hạn kích thước"
    return True, None


def _read_manifests(unit: Unit) -> str:
    chunks: list[str] = []
    for path in unit.manifests:
        try:
            chunks.append(path.read_text(encoding="utf-8", errors="ignore").lower())
        except OSError:
            continue
    return "\n".join(chunks)


def _read_sources(unit: Unit) -> str:
    """Đọc phần đầu mỗi file để nhận diện framework; không import hoặc chạy code."""
    chunks = []
    for path in unit.files[:200]:
        try:
            chunks.append(path.read_text(encoding="utf-8", errors="ignore")[:4000])
        except OSError:
            continue
    return "\n".join(chunks)


def discover(
    root: Path, excludes: tuple[str, ...]
) -> tuple[DetectedStack, list[Unit], FileInventory]:
    inventory, units = inventory_repository(root, excludes)
    services = [detect_stack(unit) for unit in units]
    analyzed = [unit for unit, service in zip(units, services) if service.analyzed]
    stack = DetectedStack(
        services=services,
        analyzed_count=sum(1 for service in services if service.analyzed),
        skipped_count=sum(1 for service in services if not service.analyzed),
    )
    return stack, analyzed, inventory


def relative_paths(unit: Unit, root: Path) -> list[str]:
    return [PurePosixPath(path.relative_to(root).as_posix()).as_posix() for path in unit.files]
