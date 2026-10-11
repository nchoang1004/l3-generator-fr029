---
uid: "01M3B99N5R829MV2SE15N4TESE"
key: API-L3GEN-003-v1
type: api-contract
group: normative
scope: system
system: SYS-L3GEN
status: draft
revision: 3
ownership: {"accountable_team":"TEAM-L3GEN","accountable_role":"tech-lead","affected_teams":[]}
relations: {"implements":["CMP-L3GEN-003"],"satisfies":["FR-L3GEN-020"],"constrained_by":["NFR-L3GEN-OPS-001"]}
verified_at: null
verified_against: []
classification: internal
ai_assisted: true
---

# Contract kiểm kê phạm vi

Giao diện nội bộ draft theo CMP-L3GEN-003 r2 ở nhánh `docs/gate-2` commit `5d06f14` (r2 chỉ đổi metadata so với r1); consumer CMP-001/004/005. Nhận Snapshot của API-L3GEN-002-v1 và ma trận hỗ trợ đã pin phiên bản, trả Inventory một lần đầy đủ. Không đọc nội dung code để suy route tại bước này.

## 1. Giao diện và trách nhiệm

`inventory(snapshot, support_matrix_version, grouping_policy_version) -> Inventory`.

`grouping_policy_version` tra policy cấu trúc nội bộ có version (tìm root/nhận diện flat); không nhận mã thực thi, URL hoặc đường dẫn từ caller. Policy này phải tương thích policy của CMP-005. **D-03 chưa chốt**: contract không ấn định root, ngưỡng hay thuật toán phân nhóm. Dùng `fixture-membership-v1` trong ví dụ tích hợp để kiểm dữ liệu mà không lựa chọn thuật toán. Thiếu policy khả dụng trả `PARTITION_POLICY_UNAVAILABLE`, không gán `flat` giả.

CMP-003 chỉ đọc manifest/config thuộc grant kiểm kê qua CMP-002; không đọc source để trích route, import hoặc body. CMP-004 sở hữu bước trích dữ kiện. Không dùng giới hạn grant để bỏ qua file âm thầm: file ngoài phạm vi có excluded/limitation tương ứng.

Đơn vị phân tích tại bước này là candidate từ manifest và cây thư mục, chưa tự chứng minh mỗi unit tương ứng chính xác một app runtime. Nhiều app khai báo trong cùng file được CMP-004 ghi bằng registration context, không đổi snapshot hay âm thầm coi mọi app là một. Monorepo có thể có nhiều candidate unit; file chung có owner unit khai báo, không bị đếm lặp.

| Trường | Nghĩa |
|---|---|
| units | Candidate unit; ID, root, ngôn ngữ/framework, mức hỗ trợ và file được xét |
| excluded | File/path bị loại và lý do, kể cả file ngoài stack |
| flat | Cây thư mục không đủ tách ít nhất hai nhóm file trong unit; heuristic có version |
| limitations | Mâu thuẫn nhận diện, manifest hỏng hoặc thiếu thông tin |
| outcome | ready, empty hoặc unsupported; hai trạng thái cuối không được đổi thành run completed rỗng |

`unit_id = "unit:" + SHA256(snapshot_id + "\n" + root_path)`; root repo là `.`. File membership unit phải duy nhất; shared file được owner khai báo rồi dùng bằng reference. Đề xuất ưu tiên root manifest sâu nhất chứa file; hòa/mâu thuẫn thì ghi limitation và giữ unit chưa kết luận, không tự đoán framework. Quy tắc này cần nhóm review trước code.

## 2. Schema

```json
{
  "$schema":"https://json-schema.org/draft/2020-12/schema",
  "$id":"https://l3gen.local/contracts/API-L3GEN-003-v1.schema.json",
  "$ref":"#/$defs/Inventory",
  "$defs":{
    "InventoryError":{
      "type":"object","additionalProperties":false,"required":["code","message","retryable"],
      "properties":{"code":{"enum":["INPUT_CONTRACT_INVALID","SNAPSHOT_MISMATCH","SNAPSHOT_UNAVAILABLE","SUPPORT_MATRIX_INVALID","PARTITION_POLICY_UNAVAILABLE","INTERNAL_INVARIANT"]},"message":{"type":"string","minLength":1},"retryable":{"const":false}}
    },
    "Inventory":{
      "type":"object","additionalProperties":false,
      "required":["schema_version","snapshot_id","support_matrix_version","grouping_policy_version","outcome","units","excluded","limitations"],
      "properties":{
        "schema_version":{"const":"0.1.0"},"snapshot_id":{"type":"string","minLength":1},
        "support_matrix_version":{"type":"string","minLength":1},"grouping_policy_version":{"type":"string","minLength":1},
        "outcome":{"enum":["ready","empty","unsupported"]},
        "units":{"type":"array","items":{
          "type":"object","additionalProperties":false,
          "required":["id","root_path","language","framework","support","file_ids","flat"],
          "properties":{
            "id":{"type":"string","minLength":1},"root_path":{"type":"string","minLength":1},
            "language":{"type":["string","null"]},"framework":{"type":["string","null"]},
            "support":{"enum":["supported","partial","unsupported","unknown"]},
            "file_ids":{"type":"array","items":{"type":"string"},"uniqueItems":true},"flat":{"type":"boolean"}
          }
        }},
        "excluded":{"type":"array","items":{
          "type":"object","additionalProperties":false,"required":["path","reason"],
          "properties":{"path":{"type":"string"},"reason":{"type":"string","minLength":1}}
        }},
        "limitations":{"type":"array","items":{"$ref":"API-L3GEN-004-v1.schema.json#/$defs/Limitation"}}
      }
    }
  }
}
```

`null` language/framework nghĩa là chưa nhận diện; phải có limitation theo unit. Không coi manifest khai dependency FastAPI là bằng chứng route đã đăng ký. Mỗi file trong snapshot phải được giải thích ở unit hoặc excluded, còn excluded ở bước intake vẫn giữ theo Snapshot. `flat` chỉ điều khiển nhánh chia nhóm theo FR-022 hiện tại, không phải điểm chất lượng kiến trúc. Khi lập BuildArchitectureInput cho CMP-005, chuyển `units[].id` thành `unit_id`, giữ `flat` và `file_ids`; chỉ chuyển file source đủ điều kiện chia nhóm, không đưa unit unsupported/rỗng vào partition. Phần không chuyển vẫn có trong inventory/limitations để không biến thành mất dữ liệu im lặng.

Để consumer vẫn thấy phạm vi bị bỏ qua sau khi snapshot hết quyền đọc, `Inventory.excluded` mang cả các entry intake từ `Snapshot.excluded` và entry bị loại khi kiểm kê, giữ lý do/phân biệt bước trong reason, loại bản sao trùng `(path,reason)`. Đường dẫn công bố là đường dẫn tương đối đã làm sạch; không đưa đường dẫn máy chủ hoặc credential vào reason. Inventory này được giữ trong VerifiedResult, không tái dựng coverage bằng cách đếm file có fact.

## 3. Lỗi và kiểm chứng

Lỗi terminal ném exception nội bộ mang payload `InventoryError`, không trộn lỗi vào Inventory. Snapshot không tồn tại/hash sai: `SNAPSHOT_UNAVAILABLE`/`SNAPSHOT_MISMATCH`, không trả Inventory khác snapshot. Manifest lỗi: trả phần biết được, limitation `MANIFEST_INVALID`. Ma trận thiếu version: `SUPPORT_MATRIX_INVALID`; không tự tuyên bố mọi framework hỗ trợ. Policy root/flat chưa chọn hoặc chưa đăng ký trả `PARTITION_POLICY_UNAVAILABLE`.

| Ca | Mong đợi |
|---|---|
| Một unit FastAPI, một unit ngôn ngữ chưa hỗ trợ | Giữ unit hỗ trợ, công bố phần ngoài phạm vi |
| Repository rỗng | outcome empty, units rỗng, run không completed |
| Hai manifest nhận diện khác nhau | Limitation, không âm thầm chọn framework |
| File chung giữa hai unit | Một owner; không hai bản cùng ID |
| Nhiều app trong một file | Inventory không bịa app runtime; CMP-004 phân biệt app context |
| D-03 chưa chọn policy / policy không khả dụng | `PARTITION_POLICY_UNAVAILABLE`; có thể kiểm consumer bằng Inventory fixture, không tuyên bố đã nhận diện root/flat thực tế |

AC-020-01/02/03. Ma trận hỗ trợ thực tế và thuật toán tìm root phải được review riêng; contract này không tự mở thêm framework.
