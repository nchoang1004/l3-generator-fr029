"""Giao diện web xem kết quả (SPEC mục 13).

Đây là lớp phủ, không phải lõi. Ba ràng buộc cứng:

1. Không bao giờ tự phân tích source. Chỉ đọc `IAM.json`, `graph.json`,
   `findings.json`, `descriptions.json` do pipeline sinh ra.
2. Xoá cả thư mục này thì dòng lệnh `l3gen <path>` vẫn chạy nguyên vẹn — lõi
   không import gì từ đây. `cli.py` chỉ import khi người dùng gõ `l3gen ui`.
3. Không hiển thị thông tin nào không có trong các file trên.
"""
