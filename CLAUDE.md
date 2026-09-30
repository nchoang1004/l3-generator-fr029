# CLAUDE.md

Trước khi làm bất cứ việc gì, luôn phải hỏi kỹ ý kiến của tôi. Nếu tự ý làm thêm phần việc mà tôi không giao, phải hỏi lại để chắc chắn, tránh tốn token mà kết quả lại không như ý.

Đây là các nguyên tắc hành xử nhằm giảm thiểu những lỗi thường gặp khi lập trình bằng LLM. Kết hợp cùng các hướng dẫn riêng của từng dự án khi cần.

## Bàn giao tự động sau mỗi thay đổi

Người dùng đã yêu cầu duy trì `docs/HANDOFF.md` thường xuyên. Việc cập nhật này trong phạm vi công việc được giao không cần hỏi lại hoặc đợi nhắc ở mỗi phiên.



- Đọc `docs/HANDOFF.md` đầu phiên để biết việc đã làm, đang dở và còn chờ duyệt. Đối chiếu code trước khi tin trạng thái cũ.
- Sau mỗi nhóm thay đổi có ý nghĩa về code, test, tài liệu, cấu hình hoặc quyết định, cập nhật hiện trạng và thêm nhật ký trong HANDOFF. Hoàn tất trước khi kết thúc phiên hoặc chuyển giao.
- Ghi ngắn: yêu cầu; file sửa; làm gì và vì sao; kết quả kiểm chứng; việc còn lại; kinh nghiệm rút ra nếu có.
- Phân biệt đề xuất, quyết định đã duyệt, code đã viết và kết quả đã đo. Test chưa chạy phải ghi chưa chạy; không dùng số đo cũ như kết quả mới.
- Cập nhật cả phần hiện trạng, không chỉ thêm nhật ký trong khi phần đầu vẫn sai. Giữ lịch sử nhật ký đã có.
- Khi phiên đã tốn nhiều token (hội thoại dài, đọc/chạy nhiều, hoặc hệ thống bắt đầu tóm tắt ngữ cảnh), đừng đợi hết ngữ cảnh: viết `docs/HANDOFF.md` đủ để phiên mới làm tiếp đúng nhịp mà không phải hỏi lại (đang làm gì, bước kế tiếp, lệnh chạy, số liệu, quy tắc đang giữ), rồi báo tôi chuyển sang phiên mới.
- Tuân theo mục “Quy tắc tự cập nhật bàn giao” trong HANDOFF. Nếu người dùng yêu cầu chỉ đọc hoặc không sửa file, không tự sửa HANDOFF; báo nội dung cần cập nhật trong chat.
- Quy tắc này không cho phép tự mở rộng tính năng, thay đổi phạm vi, commit hoặc push. CLAUDE.md là file cục bộ được ignore; không tự đưa vào commit hoặc sao chép nội dung riêng tư sang tài liệu công khai.

## Giao diện

Phần UI dùng skill `taste-skill`, lấy từ https://github.com/leonxlnx/taste-skill

- Trước khi làm bất cứ việc gì thuộc giao diện, nạp skill này và làm theo hướng dẫn trong đó.
- Skill đã cài tại `~/.claude/skills/taste-skill/SKILL.md`, gọi bằng `/taste-skill`. Trường `name:` trong file ghi là `design-taste-frontend` nhưng tên gọi lấy theo tên thư mục.
- Nếu không nạp được skill thì hỏi tôi, không tự đoán nội dung skill và không tự thiết kế thay.
- Skill quyết định cách làm UI. Các mục còn lại của CLAUDE.md vẫn áp dụng cho phạm vi, cách viết tài liệu và quy tắc bàn giao.

## 0. Cách viết tài liệu

**Lỗi đã xảy ra trong dự án này: tài liệu quá dài và nói phức tạp những chuyện đơn giản. Người đọc không theo nổi, đọc xong không biết làm gì. Tránh trước mọi thứ khác.**

### 0.1 Viết ngắn

- **Một ý nói một lần, ở một chỗ.** Chỗ khác cần thì dẫn link.
- **Viết xong đọc lại và cắt.** Bỏ mọi câu không thêm thông tin mới.
- **Nếu một mục dài quá một màn hình, nó đang làm hai việc.** Tách ra, hoặc bỏ bớt.
- Độ dài không phải giá trị. Tài liệu dài che chỗ chưa nghĩ kỹ.

### 0.2 Nói đơn giản

- **Một câu một ý. Câu ngắn.** Câu nào từ ba dấu phẩy trở lên thì tách.
- **Hạn chế từ tiếng Anh.** Chỉ giữ khi là tên riêng (FastAPI, SQLAlchemy), tên lệnh, tên file. Buộc phải dùng thuật ngữ thì giải thích ngay bằng một câu trong ngoặc, ngay lần đầu.
- **Ví dụ cụ thể thay cho mô tả trừu tượng.** Năm dòng code thường thay được cả đoạn văn.
- **Bảng và gạch đầu dòng thay cho đoạn văn dài.**
- **Mở đầu mỗi mục bằng một câu: mục này nói về cái gì.**
- **Không dùng ẩn dụ thay cho giải thích.** Chỉ dùng sau khi đã nói rõ cơ chế thật.

### 0.3 Gọi đúng tên, không thổi phồng

- Hàm duyệt cây cú pháp thì gọi là hàm duyệt cây cú pháp, không gọi là "chuyên viên trích xuất". File JSON gồm node và cạnh thì gọi đúng như vậy, không gọi là "Knowledge Graph".
- Phân biệt **đã thiết kế / đã viết code / đã chạy và đo được**. Viết xong spec không phải là làm xong tính năng. Nhật ký hôm nào chỉ sửa file markdown thì ghi thẳng là sửa tài liệu.
- Không dùng từ quảng cáo ("khoảng trống thị trường", "lợi thế cạnh tranh", "đột phá", "mạnh mẽ", "toàn diện") cho thứ chưa chạy được.
- Phát biểu về năng lực phải kèm số đo, hoặc kèm chữ "chưa đo".

Phép thử trước khi lưu một file tài liệu:

1. Người chưa biết dự án đọc một lần có hiểu không?
2. Đọc xong có biết phải làm gì tiếp không?
3. Bỏ hết tính từ và thuật ngữ đi, còn lại điều gì kiểm chứng được không?

Nếu một câu trả lời là "không", viết lại mục đó.

**Đánh đổi:** Các nguyên tắc này ưu tiên sự thận trọng hơn tốc độ. Với việc đơn giản, hãy tự linh hoạt xử lý.

## 1. Suy nghĩ kỹ trước khi viết code

**Không giả định. Không giấu sự mơ hồ. Trình bày rõ các đánh đổi.**

Trước khi triển khai:
- Nêu rõ các giả định của bạn. Nếu chưa chắc chắn, hãy hỏi.
- Nếu có nhiều cách hiểu khác nhau, trình bày tất cả — đừng tự ý chọn một cách.
- Nếu có cách làm đơn giản hơn, hãy nói ra. Phản biện khi cần thiết.
- Nếu có điều gì chưa rõ, dừng lại. Nêu rõ điểm còn vướng mắc. Hỏi lại.

## 2. Ưu tiên sự đơn giản

**Chỉ viết lượng code tối thiểu để giải quyết vấn đề. Không thêm gì mang tính suy đoán.**

- Không thêm tính năng ngoài yêu cầu.
- Không tạo abstraction cho code chỉ dùng một lần.
- Không thêm "tính linh hoạt" hay "khả năng cấu hình" nếu không được yêu cầu.
- Không xử lý lỗi cho những tình huống không thể xảy ra.
- Nếu bạn viết 200 dòng mà có thể rút gọn còn 50, hãy viết lại.

Tự hỏi: "Một kỹ sư senior có cho rằng cách này quá rườm rà không?" Nếu có, hãy đơn giản hóa.

## 3. Thay đổi có chọn lọc, chính xác

**Chỉ động vào phần cần thiết. Chỉ dọn dẹp những gì do mình gây ra.**

Khi chỉnh sửa code có sẵn:
- Không "cải thiện" code, comment hay định dạng ở phần lân cận không liên quan.
- Không refactor những chỗ không có lỗi.
- Tuân theo style hiện có, kể cả khi bạn muốn làm khác đi.
- Nếu thấy dead code không liên quan, hãy nêu ra — đừng tự ý xóa.

Khi thay đổi của bạn tạo ra phần thừa:
- Xóa các import/biến/hàm mà chính thay đổi của bạn khiến chúng không còn được dùng.
- Không xóa dead code có sẵn từ trước nếu không được yêu cầu.

Phép thử: Mỗi dòng thay đổi phải bắt nguồn trực tiếp từ yêu cầu của người dùng.

## 4. Thực thi theo mục tiêu rõ ràng

**Xác định tiêu chí thành công. Lặp lại đến khi xác minh được.**

Chuyển các yêu cầu thành mục tiêu có thể kiểm chứng:
- "Thêm validation" → "Viết test cho các input không hợp lệ, sau đó làm cho chúng pass"
- "Sửa lỗi" → "Viết một test tái hiện lỗi, sau đó làm cho nó pass"
- "Refactor X" → "Đảm bảo test pass cả trước và sau khi refactor"

Với các tác vụ nhiều bước, hãy nêu ngắn gọn kế hoạch:
```
1. [Bước] → kiểm chứng: [cách kiểm tra]
2. [Bước] → kiểm chứng: [cách kiểm tra]
3. [Bước] → kiểm chứng: [cách kiểm tra]
```

Tiêu chí thành công rõ ràng giúp bạn tự thực hiện độc lập. Tiêu chí mơ hồ (kiểu "làm sao cho chạy được") sẽ đòi hỏi phải hỏi lại liên tục.

---

**Các nguyên tắc này được xem là hiệu quả khi:** số thay đổi không cần thiết trong diff giảm đi, ít phải viết lại do làm quá phức tạp, và các câu hỏi làm rõ được đặt ra trước khi triển khai thay vì sau khi đã mắc lỗi.
</content>
</invoke>
