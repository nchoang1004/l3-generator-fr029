"""Cấu trúc dữ liệu trung gian IAM (SPEC mục 5).

Mọi bước xử lý phải tạo ra cấu trúc này trước khi sinh tài liệu. Bước sinh tài
liệu chỉ đọc từ đây, không đọc lại source.

Hai trường nhãn tách biệt, không được trộn (SPEC mục 5.1):
  - confidence:   đọc thẳng từ cú pháp (exact) hay suy từ pattern đã đặc tả (inferred)
  - completeness: đã biết đủ thuộc tính (full) hay còn phần phụ thuộc lúc chạy (partial)
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from l3gen.models.inventory import FileInventory
from l3gen.models.framework import FrameworkAnalysis
from l3gen.models.resolution import ResolutionResult
from l3gen.models.resolution import EvidenceStep, ResolutionStatus
from l3gen.models.semantic import SemanticProgram
from l3gen.models.stack import Completeness, Confidence, DetectedStack

HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE", "CONNECT"]


class SourceLocation(BaseModel):
    file: str
    line_start: int
    line_end: int


class Reference(BaseModel):
    """Một lời gọi hàm hoặc kế thừa class, kèm câu trả lời "nó trỏ tới file nào".

    resolved = False là kết quả hợp lệ, không phải lỗi. Khi đó confidence = None,
    completeness = "partial" và reason bắt buộc có (SPEC mục 5.1 quy tắc 6).
    """

    name: str
    resolved_module: str | None
    resolved: bool
    resolved_symbol: str | None = None
    """Tên đầy đủ của đích, ví dụ "app.services.order.OrderService.confirm".

    Bổ sung ngoài SPEC mục 5. Lý do: `resolved_module` chỉ cho biết FILE, không đủ
    để nối cạnh giữa hai hàm trong graph. SPEC mục 5.2 lại yêu cầu cạnh `calls`
    phải nối đúng hai node Function. Không có trường này thì phải đoán hàm nào
    trong file — sai ngay khi một file có hai hàm trùng tên."""
    confidence: Confidence | None
    completeness: Completeness
    reason: str | None
    status: ResolutionStatus | None = None
    candidate_symbols: list[str] = Field(default_factory=list)
    evidence: list[EvidenceStep] = Field(default_factory=list)
    call_fact_id: str | None = None
    location: SourceLocation | None = None
    relation: Literal["calls", "constructs", "reads", "writes", "reads_writes"] = "calls"


class APIRoute(BaseModel):
    service: str
    method: HttpMethod
    path: str
    handler_function: str
    handler_symbol: str | None = None
    calls: list[Reference]
    confidence: Confidence
    completeness: Completeness
    reason: str | None
    location: SourceLocation


class DBColumn(BaseModel):
    name: str
    type: str
    is_primary_key: bool
    foreign_key_ref: str | None


class DBEntity(BaseModel):
    service: str
    class_name: str
    table_name: str | None
    """None khi lớp không khai `__tablename__` và lớp cơ sở tự sinh tên lúc chạy.

    Ban đầu trường này luôn có giá trị: thiếu `__tablename__` thì suy theo quy ước
    tên class viết thường. Đo ở Mốc 7 cho thấy cách suy đó sai 7/9 ca trên
    Netflix/dispatch, vì lớp cơ sở của repo đó tách tên theo chữ hoa. Không có cách
    nào đọc được quy tắc ấy bằng phân tích cú pháp, nên giờ ghi None kèm `reason`
    thay vì đoán (nguyên tắc bất biến số 3, SPEC mục 5.1 quy tắc 4)."""
    columns: list[DBColumn]
    base_class: Reference | None
    confidence: Confidence
    completeness: Completeness
    reason: str | None
    location: SourceLocation


class ExternalCall(BaseModel):
    service: str
    caller_function: str
    url_or_host: str
    http_method: str | None
    inside_try_except: bool = False
    """Lời gọi có nằm trong khối try/except không.

    Bổ sung ngoài SPEC mục 5. SPEC mục 6c.3 yêu cầu đánh dấu dữ liệu này cho bước
    rà soát (category external_call_no_error_handling), nhưng không nói cất ở đâu."""
    confidence: Confidence
    completeness: Completeness
    reason: str | None
    location: SourceLocation


class FunctionNode(BaseModel):
    service: str
    qualified_name: str
    """Bổ sung ngoài SPEC mục 5, để khớp với Reference.resolved_symbol."""
    name: str
    class_name: str | None
    module: str
    calls: list[Reference]
    entity_refs: list[Reference] = Field(default_factory=list)
    """Các class bảng dữ liệu mà hàm này nhắc tới, ví dụ `db.query(Order)`.

    Bổ sung ngoài SPEC mục 5. Lý do: SPEC mục 5.2 định nghĩa cạnh `reads_writes`
    giữa hàm và bảng, nhưng IAM không có chỗ nào chứa quan hệ đó. Không có trường
    này thì không dựng được cạnh, mà graph builder lại không được đọc lại source."""
    location: SourceLocation


class UnresolvedReference(BaseModel):
    description: str
    location: SourceLocation


class ParseError(BaseModel):
    file: str
    error_message: str


class RunMetrics(BaseModel):
    """Số liệu của chính lần chạy này.

    Bất biến phải luôn đúng (SPEC mục 5):
        files_found = files_analyzed + files_skipped
        is_partial  = (files_skipped > 0) hoặc (số service bị bỏ qua > 0)
    """

    scanned_at: datetime
    files_found: int
    files_analyzed: int
    files_skipped: int
    is_partial: bool
    lines_of_code: int
    duration_seconds: float
    ai_enabled: bool
    tool_version: str
    stage_seconds: dict[str, float] = Field(default_factory=dict)
    peak_memory_bytes: int = 0


class IntermediateArchitectureModel(BaseModel):
    file_inventory: FileInventory
    semantic_program: SemanticProgram
    resolution: ResolutionResult
    framework_analysis: FrameworkAnalysis
    detected_stack: DetectedStack
    routes: list[APIRoute]
    entities: list[DBEntity]
    external_calls: list[ExternalCall]
    functions: list[FunctionNode]
    unresolved_references: list[UnresolvedReference]
    parse_errors: list[ParseError]
    metrics: RunMetrics
