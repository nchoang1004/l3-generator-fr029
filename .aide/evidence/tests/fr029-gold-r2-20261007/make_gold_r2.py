"""Write corrected gold revisions (gold.r2.json) next to the originals. The original file is never changed.

    scripts/.venv/Scripts/python.exe .aide/evidence/tests/fr029-gold-r2-20261007/make_gold_r2.py

Each correction names a JSON path (0-based), the value found there before ("<absent>" when the key is missing) and
the change. The script refuses to write when the original hash, the file of a role entry or a `before` value differs
from what was reviewed, so a correction cannot land on a gold it was not checked against. Every correction was found
by one reviewer and confirmed by a second one reading the source (listed in `confirmed_by`).
Reviews: .aide/evidence/reviews/fr029-gold-audit-20261007/ (Codex) and fr029-gold-claude-20261007/ (Claude agents).
"""
import hashlib
import json
from pathlib import Path

GOLD = Path("D:/VSF/l3-acceptance-gold")
HERE = Path(__file__).resolve().parent
ABSENT = "<absent>"
AGENT = "reworkd_platform/web/api/agent/"

CORRECTIONS = {
    "agentgpt": {
        "sha256": "d3916c80766c756fdadb6539ec19566ecb8636367824dfb9883d4057c6e3dd4b",
        "items": [
            {"id": "G01", "path": ["http_calls", 3, "accept_alt_target"],
             "before": {"kind": "literal", "value": "https://google.serper.dev/{search_type}"}, "op": "delete",
             "why": "tools/search.py:23,35: search_type là tham số, URL là f-string; mẫu chuỗi không phải URL literal.",
             "confirmed_by": ["Codex acceptance", "Codex phiên chính", "Claude accept-tdd-agentgpt"]},
            {"id": "G02", "path": ["file_roles", 57, "alt_roles"], "before": ["Khác"], "op": "delete",
             "file": AGENT + "agent_service/open_ai_agent_service.py",
             "why": "Đường gọi views.py:50 → open_ai_agent_service.py:91 → tools/tools.py:16 → tools/sidsearch.py:89 → "
                    "db/crud/oauth.py:41,47 chứng minh Service; Khác là vai trò sai.",
             "confirmed_by": ["Codex acceptance", "Codex phiên chính"]},
            {"id": "G03", "path": ["file_roles", 66, "alt_roles"], "before": ["Khác"], "op": "delete",
             "file": AGENT + "tools/tools.py", "why": "Cùng đường gọi với G02.",
             "confirmed_by": ["Codex acceptance", "Codex phiên chính"]},
            {"id": "G04", "path": ["file_roles", 55, "alt_roles"], "before": ["Khác"], "op": "delete",
             "file": AGENT + "agent_service/agent_service_provider.py",
             "why": "call_path của chính gold: views.py:39 → agent_service_provider.py:28 → dependancies.py:44 → "
                    "db/crud/agent.py:19; cùng cơ chế với G02/G03.",
             "confirmed_by": ["Claude accept-tdd-agentgpt", "Claude phiên chính (đọc call_path)"]},
            {"id": "G05", "path": ["file_roles", 50, "alt_lines"], "before": ABSENT, "op": "set", "after": [69],
             "file": AGENT + "model_factory.py",
             "why": "Gold chấp nhận vai trò thay thế Hạ tầng; dấu hiệu của vai trò đó là dòng 69 (ChatOpenAI), "
                    "nên dòng 69 phải được chấp nhận.",
             "confirmed_by": ["Claude accept-tdd-agentgpt", "Claude phiên chính"]},
            {"id": "G06", "path": ["accept_extra_limitations"], "before": ABSENT, "op": "set",
             "after": [{"kind": "unsupported_http_library",
                        "why": "SDK (openai, langchain, replicate, wikipedia) không phải thư viện HTTP; notes của gold "
                               "nói công cụ ghi chúng ở phần giới hạn thì không tính sai"}],
             "why": "Ghi quy ước trong notes thành dữ liệu cho bộ chấm; repo không có urllib/http.client/urllib3 nên "
                    "không che mất lỗi thật.",
             "confirmed_by": ["Claude accept-tdd-agentgpt", "Claude phiên chính (đọc 10 dòng)"]},
            {"id": "G07", "bulk": "khac_line_null",
             "why": "Vai trò Khác không có dấu hiệu, dòng nào cũng được (như gold kibo: line null); gold cũ bắt đúng "
                    "một dòng tùy chọn.",
             "confirmed_by": ["Claude accept-tdd-agentgpt", "Claude phiên chính (đối chiếu quy ước kibo)"]},
        ],
    },
    "kibo": {
        "sha256": "db831c31453fc5bf365db5f14a154cc8b8986800a30fe67e9fa6576bed7836f1",
        "items": [
            {"id": "K01", "path": ["file_roles", 105, "alt_lines"], "before": [70, 113, 120, 136, 151, 186, 191],
             "op": "set", "after": [38, 70, 113, 120, 136, 151, 186, 191, 307, 314, 332],
             "file": "app/services/scheduler/reminder_scheduler.py",
             "why": "db.close() ở dòng 38, 307, 314, 332 là gọi method trên session; gold tính db.close() là truy cập "
                    "dữ liệu ở file_roles[125].",
             "confirmed_by": ["Claude accept-kibo", "Claude phiên chính (đọc 4 dòng)"]},
            {"id": "K02", "path": ["file_roles", 55, "alt_lines"], "op": "extend", "after": [414, 426],
             "file": "app/repositories/appointments/appointment_repository.py",
             "why": "Dòng 414, 426: update(Appointment) dựng truy vấn.",
             "confirmed_by": ["Claude accept-kibo", "Claude phiên chính (đọc 2 dòng)"]},
        ],
    },
}


def _at(doc, path):
    for p in path[:-1]:
        doc = doc[p]
    return doc, path[-1]


def _apply(case, gold, c):
    if c.get("bulk") == "khac_line_null":
        n = 0
        for x in gold["file_roles"]:
            if x["role"] == "Khác" and not x.get("alt_roles") and x.get("line") is not None:
                x["line"] = None
                x.pop("alt_lines", None)
                n += 1
        c["count"] = n
        return
    parent, last = _at(gold, c["path"])
    if "file" in c and parent.get("file") != c["file"]:
        raise SystemExit(f"{case} {c['id']}: {c['path']} không phải {c['file']}")
    if c["op"] == "extend":
        parent[last] = sorted(set(parent.get(last, [])) | set(c["after"]))
        return
    if parent.get(last, ABSENT) != c["before"]:
        raise SystemExit(f"{case} {c['id']}: giá trị tại {c['path']} khác bản đã kiểm")
    if c["op"] == "delete":
        del parent[last]
    else:
        parent[last] = c["after"]


def main():
    out = []
    for case, spec in CORRECTIONS.items():
        src = GOLD / case / "gold.json"
        raw = src.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != spec["sha256"]:
            raise SystemExit(f"{case}: gold.json đã đổi ({digest}), không áp đính chính")
        gold = json.loads(raw.decode("utf-8"))
        for c in spec["items"]:
            _apply(case, gold, c)
        gold["revision"] = 2
        gold["revision_of"] = {"file": "gold.json", "sha256": digest}
        gold["corrections"] = spec["items"]
        dst = GOLD / case / "gold.r2.json"
        text = json.dumps(gold, ensure_ascii=False, indent=2) + "\n"
        dst.write_text(text, encoding="utf-8")
        out.append({"case": case, "from": str(src), "from_sha256": digest, "to": str(dst),
                    "to_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "corrections": [c["id"] + (f" ({c['count']} mục)" if "count" in c else "") for c in spec["items"]]})
    (HERE / "written.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
