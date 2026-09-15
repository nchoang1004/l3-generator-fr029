"""Chia repo thành các đơn vị phân tích và nhận diện stack từng đơn vị (bước 1b).

Vì sao không coi cả repo là một khối: một hệ thống thật thường có nhiều service
với stack khác nhau. Nếu chọn ngôn ngữ theo số file chiếm đa số thì repo có ứng
dụng Java lớn kèm một service FastAPI nhỏ sẽ bị kết luận là "project Java", và
service FastAPI bị bỏ hoàn toàn — im lặng, không cảnh báo (SPEC mục 4.4).

Ranh giới service lấy theo vị trí file manifest, vì manifest là tuyên bố tường
minh của người viết code rằng "đây là một đơn vị triển khai độc lập". Đếm tỷ lệ
file chỉ là suy đoán, và suy đoán đó sai ngay khi hai service lệch nhau về quy mô.
"""

from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

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

EXTENSION_LANGUAGE = {".py": "python", ".java": "java", ".go": "go", ".ts": "javascript"}

SUPPORTED_LANGUAGE = "python"
SUPPORTED_FRAMEWORK = "fastapi"

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
    """Một đơn vị phân tích trước khi nhận diện stack."""

    root: Path
    rel_root: str
    manifest: str | None
    language: str
    files: list[Path] = field(default_factory=list)


def find_units(root: Path, excludes: tuple[str, ...]) -> list[Unit]:
    """Tìm ranh giới service theo vị trí manifest.

    Manifest lồng nhau thì đơn vị con thắng: mỗi file thuộc về manifest gần nó
    nhất tính từ dưới lên.
    """
    excluded = set(excludes)

    def is_visible(path: Path) -> bool:
        return excluded.isdisjoint(path.relative_to(root).parts[:-1])

    markers: dict[Path, tuple[str, str]] = {}
    for name, language in MANIFESTS.items():
        for found in root.rglob(name):
            if found.is_file() and is_visible(found):
                markers.setdefault(found.parent, (name, language))

    if not markers:
        markers[root] = ("", "")

    units = {
        directory: Unit(
            root=directory,
            rel_root=_relative(directory, root),
            manifest=name or None,
            language=language,
        )
        for directory, (name, language) in markers.items()
    }

    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in EXTENSION_LANGUAGE or not is_visible(path):
            continue
        owner = _nearest_unit(path.parent, units)
        if owner is not None:
            owner.files.append(path)

    for unit in units.values():
        if not unit.language:
            unit.language = _majority_language(unit.files)
        # Chỉ giữ file của ngôn ngữ chính. File ngôn ngữ khác nằm ngoài phạm vi
        # parser của đơn vị này, không được tính là lỗi cú pháp (SPEC mục 4.4.3).
        unit.files = [
            f for f in unit.files if EXTENSION_LANGUAGE.get(f.suffix) == unit.language
        ]

    return [u for u in units.values() if u.files]


def _nearest_unit(directory: Path, units: dict[Path, Unit]) -> Unit | None:
    """Manifest gần nhất tính từ thư mục này đi lên."""
    current = directory
    while True:
        if current in units:
            return units[current]
        if current.parent == current:
            return None
        current = current.parent


def _majority_language(files: list[Path]) -> str:
    counts: dict[str, int] = {}
    for path in files:
        language = EXTENSION_LANGUAGE.get(path.suffix)
        if language:
            counts[language] = counts.get(language, 0) + 1
    return max(counts, key=counts.get) if counts else ""


def _relative(path: Path, root: Path) -> str:
    rel = path.relative_to(root).as_posix()
    return rel if rel != "." else ""


def detect_stack(unit: Unit) -> ServiceUnit:
    """Nhận diện framework và ORM của một đơn vị, từ hai nguồn bằng chứng."""
    manifest_text = _read_manifest(unit)
    source_text = _read_sources(unit)

    frameworks: list[str] = []
    in_manifest: list[str] = []
    in_source: list[str] = []

    for framework, markers in FRAMEWORK_IMPORT_MARKERS.items():
        from_manifest = any(
            m in manifest_text for m in FRAMEWORK_MANIFEST_MARKERS.get(framework, ())
        )
        from_source = any(m in source_text for m in markers)
        if from_manifest or from_source:
            frameworks.append(framework)
            if from_manifest:
                in_manifest.append(framework)
            if from_source:
                in_source.append(framework)

    orm = next(
        (name for name, markers in ORM_MARKERS.items()
         if any(m in manifest_text or m in source_text for m in markers)),
        None,
    )

    completeness, reason = _evidence_note(unit, frameworks, in_manifest, in_source)
    analyzed, skip_reason = _support_decision(unit, frameworks)

    return ServiceUnit(
        name=unit.rel_root or unit.root.name,
        root_path=unit.rel_root,
        manifest_file=unit.manifest,
        language=unit.language,
        frameworks=sorted(frameworks),
        orm=orm,
        confidence="exact",
        completeness=completeness,
        detection_reason=reason,
        file_count=len(unit.files),
        analyzed=analyzed,
        skip_reason=skip_reason,
    )


def _evidence_note(unit, frameworks, in_manifest, in_source) -> tuple[str, str]:
    if not frameworks:
        return "partial", (
            f"ngôn ngữ {unit.language or 'chưa rõ'} suy từ phần mở rộng file; "
            "chưa thấy dấu hiệu framework nào"
        )
    if not unit.manifest:
        return "partial", (
            f"thấy {', '.join(in_source)} trong source; "
            "không tìm thấy file khai báo phụ thuộc"
        )
    only_manifest = [f for f in frameworks if f not in in_source]
    if only_manifest:
        return "partial", (
            f"{', '.join(only_manifest)} có trong {unit.manifest} "
            "nhưng chưa thấy dùng trong source"
        )
    return "full", f"{', '.join(sorted(frameworks))} có trong {unit.manifest} và trong source"


def _support_decision(unit: Unit, frameworks: list[str]) -> tuple[bool, str | None]:
    if unit.language != SUPPORTED_LANGUAGE:
        return False, f"ngôn ngữ {unit.language or 'chưa rõ'} chưa được hỗ trợ"
    if SUPPORTED_FRAMEWORK not in frameworks:
        found = ", ".join(frameworks) if frameworks else "không nhận ra framework nào"
        return False, f"chỉ hỗ trợ {SUPPORTED_FRAMEWORK}; đơn vị này: {found}"
    return True, None


def _read_manifest(unit: Unit) -> str:
    if unit.manifest is None:
        return ""
    try:
        return (unit.root / unit.manifest).read_text(encoding="utf-8", errors="ignore").lower()
    except OSError:
        return ""


def _read_sources(unit: Unit) -> str:
    """Đọc phần đầu mỗi file để tìm dấu hiệu framework. Chỉ đọc, không chạy."""
    chunks = []
    for path in unit.files[:200]:
        try:
            chunks.append(path.read_text(encoding="utf-8", errors="ignore")[:4000])
        except OSError:
            continue
    return "\n".join(chunks)


def discover(root: Path, excludes: tuple[str, ...]) -> tuple[DetectedStack, list[Unit]]:
    """Chia repo thành đơn vị và nhận diện stack từng cái.

    Trả về DetectedStack chứa TẤT CẢ đơn vị (kể cả bị bỏ qua) và danh sách đơn vị
    sẽ được phân tích. Đơn vị bị bỏ qua vẫn xuất hiện trong tài liệu kèm lý do —
    im lặng bỏ qua một service là kiểu thất bại tệ nhất.
    """
    units = sorted(find_units(root, excludes), key=lambda u: u.rel_root)
    services = [detect_stack(u) for u in units]

    analyzed = [u for u, s in zip(units, services) if s.analyzed]
    stack = DetectedStack(
        services=services,
        analyzed_count=sum(1 for s in services if s.analyzed),
        skipped_count=sum(1 for s in services if not s.analyzed),
    )
    return stack, analyzed


def relative_paths(unit: Unit, root: Path) -> list[str]:
    return [PurePosixPath(p.relative_to(root).as_posix()).as_posix() for p in unit.files]
