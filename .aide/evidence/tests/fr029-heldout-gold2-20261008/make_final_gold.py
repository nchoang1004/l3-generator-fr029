"""Final golds of the four new held-out repositories (08/10/2026), from two independent writers per repository.

    scripts/.venv/Scripts/python.exe .aide/evidence/tests/fr029-heldout-gold2-20261008/make_final_gold.py

Writer A (Claude Opus) and writer B (Claude Sonnet) each read the source alone, without the other's file or any tool
output. `slice/tools/fr029_gold_diff.py` lists their disagreements; each one was settled by reading the source
(see RECONCILED). The final gold is A's file with the decisions recorded in it; A and B stay as they are.
Also writes membership.json: one normal component holding every non-empty .py file of the snapshot.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "slice"))
sys.path.insert(0, str(ROOT / "slice" / "tools"))

from l3slice import snapshot  # noqa: E402
import fr029_gold_diff  # noqa: E402

GOLD = Path("D:/VSF/l3-heldout-gold2")
REPOS = Path("D:/VSF/l3-heldout-repos2")
RECONCILED = {
    "BlackIQ_tgju-api": ["http_calls: B ghi scrap/tgju.py:279, nhưng file chỉ có 134 dòng; lời gọi client.get(url) ở dòng 27 "
                         "(A đúng)."],
    "gabryelvs_fx-service": [],
    "AlexGoster_orderflow-services": ["http_calls catalog_client.py:98 target: A ghi config catalog_service_url, B ghi unknown; "
                                      "mỗi bản đã khai cách hiểu kia ở accept_alt_target, nên hai đáp án đều được chấp nhận."],
    "zolderio_token-proxy": ["routes catch-all: A ghi /session/{session_id}/{path:path} (dạng source), B ghi dạng OpenAPI "
                             "{path}; cùng một endpoint, bộ chấm chuẩn hóa converter (fr029_score._route_path)."],
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    out = []
    for name, decisions in RECONCILED.items():
        a_path, b_path = GOLD / name / "gold-A.json", GOLD / name / "gold-B.json"
        a = json.loads(a_path.read_text(encoding="utf-8"))
        b = json.loads(b_path.read_text(encoding="utf-8"))
        diffs = fr029_gold_diff.compare(a, b)
        final = dict(a)
        final["provenance"] = {
            "writers": {"A": "Claude Opus, độc lập", "B": "Claude Sonnet, độc lập"},
            "A_sha256": sha(a_path), "B_sha256": sha(b_path), "disagreements": diffs, "decisions": decisions,
            "reviewed_by_human": False, "seen_tool_output": False}
        (GOLD / name / "gold.json").write_text(json.dumps(final, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        src = REPOS / name / final.get("root", ".")
        snap, _ = snapshot.take(src)
        py = [f["path"] for f in snap["files"] if f["path"].endswith(".py") and f["byte_size"]]
        membership = {"partition_version": "fixture-membership-v1", "components": [
            {"name": "Toàn bộ", "kind": "normal", "files": py},
            {"name": "Khác", "kind": "other", "files": [f["path"] for f in snap["files"] if f["path"] not in set(py)]}]}
        (GOLD / name / "membership.json").write_text(json.dumps(membership, ensure_ascii=False), encoding="utf-8")
        out.append({"repo": name, "disagreements": len(diffs), "routes": len(final["routes"]),
                    "models": len(final.get("models", [])), "http_calls": len(final.get("http_calls", [])),
                    "gold_sha256": sha(GOLD / name / "gold.json")})
    (Path(__file__).parent / "written.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
