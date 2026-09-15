"""Khoá cứng dạng dữ liệu AI được phép trả về (SPEC mục 8.3, 8.4).

Đây là cái khoá cửa: dù AI có "sáng tạo" đến đâu cũng không có trường nào để chèn
thêm route, bảng dữ liệu hay quan hệ vào IAM. Nó chỉ điền được đúng hai thứ —
một đoạn mô tả bằng lời, và một câu tóm tắt cho cảnh báo đã được phát hiện sẵn.

Ngoài khoá schema, còn một lớp chặn thứ hai ở tầng thiết kế: mô tả do AI viết
được ghi ra file riêng (`descriptions.json`), không nằm trong `IAM.json`. Nhờ vậy
chạy có AI và không AI cho ra `IAM.json` giống hệt từng byte — kiểm chứng được
bằng lệnh `diff`, không phải bằng lòng tin.
"""

from pydantic import BaseModel, Field

MAX_DESCRIPTION_CHARS = 400


class Description(BaseModel):
    """Mô tả cho đúng một thực thể đã có sẵn trong IAM."""

    target_id: str
    """Mã của thực thể. AI phải chọn từ danh sách được đưa vào, không được bịa."""
    text: str = Field(max_length=MAX_DESCRIPTION_CHARS)


class DescriptionBatch(BaseModel):
    descriptions: list[Description]


class FindingSummary(BaseModel):
    """Câu tóm tắt cho một cảnh báo mà phần tĩnh đã phát hiện.

    AI không quyết định cảnh báo nào được tạo — nó chỉ diễn đạt lại cho dễ đọc.
    """

    finding_id: str
    summary: str = Field(max_length=MAX_DESCRIPTION_CHARS)


class FindingSummaryBatch(BaseModel):
    summaries: list[FindingSummary]
