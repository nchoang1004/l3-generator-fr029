"""Tên module suy từ package Python; folder chứa package không phải service."""

from collections import Counter
from pathlib import PurePosixPath


def module_map(paths: list[str]) -> dict[str, str]:
    packages = {
        str(PurePosixPath(path).parent)
        for path in paths if PurePosixPath(path).name in ("__init__.py", "__init__.pyi")
    }
    result = {}
    for path in paths:
        source = PurePosixPath(path)
        directory = source.parent
        top_package = None
        while True:
            if str(directory) in packages:
                top_package = directory
            if directory == directory.parent:
                break
            directory = directory.parent
        if top_package is not None:
            relative = source.relative_to(top_package.parent)
        else:
            parts = source.parts
            # src là convention source root; không kết luận service boundary.
            relative = PurePosixPath(*parts[parts.index("src") + 1:]) if "src" in parts else source
        segments = list(relative.parts[:-1])
        if source.stem != "__init__":
            segments.append(source.stem)
        result[path] = ".".join(segments)
    counts = Counter(result.values())
    # Hai source root cùng khai app.main: không gộp symbol. Giữ namespace file
    # riêng; import nhập nhằng sẽ không nối cho tới khi có cấu hình source root.
    for path, module in list(result.items()):
        if counts[module] > 1:
            result[path] = "@file:" + path
    return result
