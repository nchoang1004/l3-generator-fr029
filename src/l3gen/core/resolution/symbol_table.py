"""Hai bảng tra cứu — nền tảng của mọi việc nối tham chiếu.

Cây cú pháp cho biết TÊN, không cho biết NGHĨA. Nhìn `svc.confirm()` chỉ biết có
một biến tên `svc` và một method tên `confirm`. Hai bảng dưới đây bắc cầu từ tên
sang nghĩa.

Bảng 1 — danh bạ: ai định nghĩa ở đâu (toàn repo).
Bảng 2 — tên gọi trong từng file: trong file này thì `OrderService` nghĩa là gì.

Bảng 2 BẮT BUỘC tách riêng theo từng file. File A có thể lấy `OrderService` từ
`app.services.order`, file B lấy cùng tên đó từ `legacy.service`. Gộp chung một
bảng thì graph vẫn đẹp, test vẫn qua, chỉ có vài cạnh trỏ nhầm file mà không cách
nào phát hiện (SPEC mục 15.3). Đây là lỗi thiết kế nguy hiểm nhất của dự án.
"""

from dataclasses import dataclass, field

KIND_CLASS = "class"
KIND_FUNCTION = "function"
KIND_METHOD = "method"
KIND_ASSIGN = "assign"


@dataclass(frozen=True)
class Definition:
    """Một thứ được định nghĩa ở đâu đó trong repo."""

    qualified_name: str
    rel_path: str
    line: int
    kind: str


@dataclass
class DefinitionIndex:
    """Bảng 1 — danh bạ.

    known_modules chứa mọi module và package tìm thấy trong repo. Dùng để phân
    biệt "tên này của repo" với "tên này của thư viện ngoài".
    """

    definitions: dict[str, Definition] = field(default_factory=dict)
    known_modules: set[str] = field(default_factory=set)
    _methods: dict[str, dict[str, Definition]] = field(default_factory=dict)

    def add(self, definition: Definition) -> None:
        self.definitions[definition.qualified_name] = definition
        if definition.kind == KIND_METHOD:
            class_qname, _, method_name = definition.qualified_name.rpartition(".")
            self._methods.setdefault(class_qname, {})[method_name] = definition

    def get(self, qualified_name: str) -> Definition | None:
        return self.definitions.get(qualified_name)

    def method_of(self, class_qname: str, method_name: str) -> Definition | None:
        return self._methods.get(class_qname, {}).get(method_name)

    def is_internal(self, qualified_name: str) -> bool:
        """Tên này thuộc repo đang quét, hay là thư viện ngoài?"""
        if qualified_name in self.definitions or qualified_name in self.known_modules:
            return True
        root = qualified_name.split(".")[0]
        return root in self.known_modules


@dataclass
class FileScope:
    """Bảng 2 cho MỘT file: tên viết trong file này ứng với tên đầy đủ nào.

    Gồm cả tên do file tự định nghĩa lẫn tên lấy về qua import. Tên tự định nghĩa
    được ưu tiên, đúng như Python thật.
    """

    rel_path: str
    module_name: str
    names: dict[str, str] = field(default_factory=dict)
    has_wildcard_import: bool = False

    def resolve(self, name: str) -> str | None:
        """Tên ngắn viết trong file này trỏ tới tên đầy đủ nào. None nếu không biết."""
        return self.names.get(name)


@dataclass
class ImportTables:
    """Bảng 2 của mọi file. Chỉ tra được theo từng file, không có bảng dùng chung."""

    by_file: dict[str, FileScope] = field(default_factory=dict)

    def for_file(self, rel_path: str) -> FileScope | None:
        return self.by_file.get(rel_path)
