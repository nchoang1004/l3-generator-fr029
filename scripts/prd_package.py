#!/usr/bin/env python3
"""Sinh và kiểm Change Set View từ baseline candidate.

Hai lệnh:

    py -3.12 scripts/prd_package.py render --change-set CHG-L3GEN-2026-002 --baseline BL-r1.yaml
    py -3.12 scripts/prd_package.py check  --change-set CHG-L3GEN-2026-002 --baseline BL-r1.yaml

`--change-set` bắt buộc khi có nhiều hơn một Change Set.

`render` đọc baseline, lấy đúng các artifact có trong đó, rồi ghi
`.aide/generated/change-set-views/CSV-<CHG-key>.md` theo bảy mục ở EXEC §D.1b.
`check` không ghi gì, chỉ đối chiếu baseline với file nguồn và báo lệch.

Recovery review (EXEC §B.17): đã sửa artifact sau review thì lập baseline mới và chạy
`render --recovery`. View ghi ra `CSV-<CHG-key>-<rN>.md`, view đã review giữ nguyên.

Ràng buộc đã áp:

- View là `group: derived`, `non_normative: true`; nguồn thắng khi bất đồng.
- Nội dung chỉ lấy từ file nguồn, không chép tay và không tự đặt số liệu.
- Từ chối ghi đè khi đã có review hoặc approval, theo EXEC §B.17 review freeze.
- Baseline không khớp file thật thì dừng; không render bản sai rồi ghi chú sau.

Script này là bản viết lại trong repo, không phải công cụ `aide` chính thức.
Nó đọc frontmatter cục bộ trong `.aide/`, không đọc metadata graph tập trung.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AIDE = REPO / ".aide"
CHANGE_SETS = AIDE / "lifecycle" / "change-sets"
VIEWS = AIDE / "generated" / "change-set-views"

# Giữ thứ tự hiển thị theo nhóm, không theo thứ tự xuất hiện trong baseline.
FR_RE = re.compile(r"^FR-")
NFR_RE = re.compile(r"^NFR-")


class Problem(Exception):
    """Lỗi dừng hẳn — in ra rồi thoát mã 1."""


# --------------------------------------------------------------------------
# Đọc dữ liệu
# --------------------------------------------------------------------------


def read_bytes(path: Path) -> bytes:
    if not path.exists():
        raise Problem(f"không có file {rel(path)}")
    return path.read_bytes()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO)).replace("\\", "/")
    except ValueError:
        return str(path)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def frontmatter(raw: bytes) -> dict[str, str]:
    """Lấy các trường vô hướng ở frontmatter.

    Không dùng thư viện YAML: frontmatter ở đây chỉ gồm khóa đơn giản và vài
    khóa có giá trị JSON một dòng (`ownership`, `relations`). Đọc bằng regex
    giữ script chạy được khi máy không cài PyYAML.
    """
    text = raw.decode("utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict[str, str] = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"')
    return out


def parse_baseline(path: Path) -> dict:
    """Đọc baseline YAML ở phạm vi cấu trúc mà file này thật sự dùng."""
    text = read_bytes(path).decode("utf-8")
    head: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("artifacts:"):
            break
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            head[m.group(1)] = m.group(2).strip()

    artifacts = []
    for m in re.finditer(
        r"- key: (\S+)\n  revision: (\d+)\n  path: (\S+)\n  sha256: (\S+)", text
    ):
        artifacts.append(
            {
                "key": m.group(1),
                "revision": int(m.group(2)),
                "path": m.group(3),
                "sha256": m.group(4),
            }
        )
    if not artifacts:
        raise Problem(f"{rel(path)} không có artifact nào đọc được")
    return {"head": head, "artifacts": artifacts}


def parse_change_set(path: Path) -> dict[str, str]:
    text = read_bytes(path).decode("utf-8")
    out: dict[str, str] = {}
    for line in text.splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"')
    return out


def body_after_frontmatter(raw: bytes) -> str:
    text = raw.decode("utf-8")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4 :]
    return text.lstrip("\r\n")


def section(text: str, heading: str) -> str:
    """Cắt một mục cấp 2 khỏi thân artifact, bỏ dòng tiêu đề.

    `heading` khớp theo tiền tố vì PRD rút gọn tên mục so với mẫu
    (ví dụ "2. Ngoài phạm vi phiên bản đầu" thay cho "2. Ngoài phạm vi
    (Out of Scope)"). Số thứ tự lặp lại giữa các phần I–IX nên chỉ lấy
    lần khớp đầu tiên là chưa đủ — người gọi truyền tiền tố đủ dài để
    duy nhất.
    """
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}[^\n]*$(.*?)(?=^##\s+|\Z)", re.M | re.S
    )
    m = pattern.search(text)
    return m.group(1).strip() if m else ""


def demote(text: str, levels: int = 2) -> str:
    """Hạ heading để lồng vừa vào cấu trúc view.

    Artifact nguồn mở đầu bằng `#`; view đã dùng `#` cho tiêu đề và `##` cho
    bảy mục, nên thân artifact phải bắt đầu từ `###` trở xuống.
    """
    return re.sub(
        r"^(#{1,4})\s", lambda m: "#" * (len(m.group(1)) + levels) + " ", text, flags=re.M
    )


# --------------------------------------------------------------------------
# Kiểm
# --------------------------------------------------------------------------


def verify(baseline: dict) -> list[str]:
    """Đối chiếu baseline với file nguồn. Trả về danh sách lệch."""
    issues: list[str] = []
    seen_uids = set()
    seen_keys = set()
    for art in baseline["artifacts"]:
        path = REPO / art["path"]
        if not path.exists():
            issues.append(f"{art['key']}: không có file {art['path']}")
            continue
        raw = path.read_bytes()
        if sha256(raw) != art["sha256"]:
            issues.append(f"{art['key']}: sha256 lệch so với file thật")
        fm = frontmatter(raw)
        uid = fm.get("uid", "")
        if not re.fullmatch(r"[0-7][0-9A-HJKMNP-TV-Z]{25}", uid):
            issues.append(f"{art['key']}: UID thiếu hoặc sai ULID")
        if uid in seen_uids:
            issues.append(f"{art['key']}: UID trùng")
        seen_uids.add(uid)
        if art['key'] in seen_keys or fm.get('key') != art['key']:
            issues.append(f"{art['key']}: key trùng hoặc không khớp")
        seen_keys.add(art['key'])
        actual = fm.get("revision")
        if actual is not None and actual != str(art["revision"]):
            issues.append(
                f"{art['key']}: baseline ghi revision {art['revision']}, file thật {actual}"
            )
    return issues


def guard_review_freeze(chg_key: str, baseline_key: str | None = None) -> None:
    """Có review hoặc approval của Change Set này rồi thì không ghi đè view.

    EXEC §B.17: từ lúc ghi receipt tới lúc approve, cấm ghi vào artifact đã
    review. Xoá evidence để vượt kiểm là sai quy trình, nên script chỉ dừng
    và báo, không tự xử lý. Evidence của Change Set khác không chặn.

    `baseline_key` dùng cho recovery review: view ghi ra file riêng, nên chỉ
    chặn khi review hoặc approval đã nhắm đúng baseline đó.
    """
    for name in ("reviews", "approvals"):
        folder = AIDE / "evidence" / name
        if not folder.exists():
            continue
        for p in folder.iterdir():
            if not p.is_file():
                continue
            text = p.read_text(encoding="utf-8")
            if f"change_set: {chg_key}" not in text:
                continue
            if baseline_key is None or re.search(
                rf"^baseline: {re.escape(baseline_key)}\s*$", text, re.M
            ):
                raise Problem(
                    f"có file trong evidence/{name}/ — đang trong vòng review.\n"
                    "  Dùng quy trình re-review chính thức (--recovery với baseline mới), không ghi đè view."
                )


# --------------------------------------------------------------------------
# Render
# --------------------------------------------------------------------------


def source_line(art: dict) -> str:
    fm = frontmatter(read_bytes(REPO / art["path"]))
    # Đường dẫn tương đối tính từ generated/change-set-views/ về gốc .aide/
    link = "../../" + art["path"].removeprefix(".aide/")
    return (
        f"Nguồn: [{art['key']}]({link}) · revision {art['revision']} · "
        f"status {fm.get('status', '?')} · SHA-256 `{art['sha256']}`"
    )


def rebase_links(body: str, art_path: str) -> str:
    """Đổi gốc các link tương đối trong thân artifact sang vị trí của view.

    Link trong file nguồn viết theo thư mục của chính nó (ví dụ `../nfr/...`
    trong một FR). Nhúng nguyên văn vào view ở `generated/change-set-views/`
    thì trỏ sai. Tính lại đích thật rồi viết lại đường dẫn từ thư mục view.
    """
    src_dir = (REPO / art_path).parent
    view_dir = VIEWS

    def fix(m: re.Match[str]) -> str:
        target = (src_dir / m.group(2)).resolve()
        if not target.exists():
            return m.group(0)  # link vốn đã hỏng ở nguồn — không tự sửa
        new = os.path.relpath(target, view_dir).replace("\\", "/")
        return f"[{m.group(1)}]({new})"

    return re.sub(r"\[([^\]]+)\]\((\.\.?/[^)]+)\)", fix, body)


def render_artifact(art: dict) -> str:
    raw = read_bytes(REPO / art["path"])
    body = rebase_links(body_after_frontmatter(raw), art["path"])
    # Bỏ mục "Tài liệu liên quan": view đã có link nguồn ở dòng trên.
    body = re.sub(r"^##\s+Tài liệu liên quan\s*$.*", "", body, flags=re.M | re.S).rstrip()
    return "---\n\n" + source_line(art) + "\n\n" + demote(body) + "\n"


def render_open_questions(chg_dir: Path) -> str:
    """Chỉ liệt OQ chưa đóng, theo §D.1b mục 7."""
    rows = []
    for path in sorted((chg_dir / "open-questions").glob("OQ-*.md")):
        fm = frontmatter(read_bytes(path))
        if fm.get("status", "").strip('"') in {"closed", "cancelled"}:
            continue
        text = body_after_frontmatter(read_bytes(path))
        m = re.search(r"^#\s+(.+)$", text, re.M)
        title = m.group(1).split("—", 1)[-1].strip() if m else path.stem
        link = f"../../lifecycle/change-sets/{chg_dir.name}/open-questions/{path.name}"
        rows.append(
            f"| [{path.stem}]({link}) | {title} | {fm.get('owner', '')} | {fm.get('due', '')} | {fm.get('status', '')} |"
        )
    if not rows:
        return "Không còn câu hỏi mở.\n"
    head = "| OQ | Câu hỏi | Owner | Due | Status |\n|---|---|---|---|---|\n"
    return head + "\n".join(rows) + "\n"


def pick_change_set(key: str | None) -> Path:
    chg_dirs = [p for p in CHANGE_SETS.iterdir() if p.is_dir()]
    if key:
        target = CHANGE_SETS / key
        if not target.is_dir():
            raise Problem(f"không có Change Set {key} trong {rel(CHANGE_SETS)}")
        return target
    if len(chg_dirs) != 1:
        raise Problem(
            f"có {len(chg_dirs)} Change Set trong {rel(CHANGE_SETS)}; truyền --change-set"
        )
    return chg_dirs[0]


def render(baseline_name: str, chg_key: str | None, recovery: bool = False) -> Path:
    chg_dir = pick_change_set(chg_key)
    chg = parse_change_set(chg_dir / "change-set.yaml")

    baseline_path = chg_dir / "baseline" / baseline_name
    baseline = parse_baseline(baseline_path)

    issues = verify(baseline)
    if issues:
        raise Problem(
            "baseline không khớp file nguồn, không render:\n"
            + "\n".join(f"  - {i}" for i in issues)
        )

    bl_key = baseline["head"].get("key", baseline_name)
    guard_review_freeze(chg["key"], bl_key if recovery else None)
    view_key = f"CSV-{chg['key']}"
    if recovery:
        view_key += "-" + Path(baseline_name).stem.removeprefix("BL-")

    arts = baseline["artifacts"]
    frs = [a for a in arts if FR_RE.match(a["key"])]
    nfrs = [a for a in arts if NFR_RE.match(a["key"])]
    prd = next((a for a in arts if a["key"].startswith("PRD-")), None)
    frs.sort(key=lambda a: a["key"])
    nfrs.sort(key=lambda a: a["key"])

    label = chg.get("label", chg.get("key", "Change Set"))

    out: list[str] = []
    out.append("---")
    out.append(f"key: {view_key}")
    out.append("group: derived")
    out.append("non_normative: true")
    out.append(f"derived_from: [{bl_key}]")
    out.append("hand_written: false")
    out.append("status: candidate")
    out.append(f"generated_by: scripts/prd_package.py render --baseline {baseline_name}"
               + (" --recovery" if recovery else ""))
    out.append("---")
    out.append("")
    out.append(f"# {label}")
    out.append("")
    out.append(
        f"Bản ứng viên chưa duyệt, sinh từ `{bl_key}`. Khi view và nguồn bất đồng, "
        "**FR/NFR/PRD nguồn thắng**; sửa nguồn rồi chạy lại script render. "
        "Không dùng view này như approval."
    )
    out.append("")
    out.append(
        f"Gồm {len(frs)} FR, {len(nfrs)} NFR và "
        f"{sum(1 for a in arts if a['key'].startswith('OBS-'))} OBS trong baseline."
    )
    out.append("")

    # 1
    out.append("## 1. Mục tiêu")
    out.append("")
    if prd:
        goals = section(
            rebase_links(body_after_frontmatter(read_bytes(REPO / prd["path"])), prd["path"]),
            "3. Mục tiêu kinh doanh",
        )
        out.append(goals if goals else f"Xem PRD `{prd['key']}` revision {prd['revision']}.")
    else:
        out.append(chg.get("note", "Chưa có PRD trong baseline."))
    out.append("")

    # 2
    out.append("## 2. Mục tiêu nghiệp vụ đổi")
    out.append("")
    if chg.get("supersedes"):
        out.append(
            f"Change Set này thay cho `{chg['supersedes']}`. Mọi GOAL/KPI mang key mới; "
            "GOAL/KPI của Change Set cũ không còn hiệu lực. GOAL hiện hành ở mục 1, KPI hiện hành dưới đây."
        )
        if prd:
            kpis = section(
                rebase_links(body_after_frontmatter(read_bytes(REPO / prd["path"])), prd["path"]),
                "4. Chỉ số thành công",
            )
            if kpis:
                out.append("")
                out.append(kpis)
    else:
        out.append(
            "Chưa có baseline đã approved để so diff — đây là baseline candidate đầu tiên "
            "của một System mới, nên toàn bộ GOAL/KPI ở PRD đều là bản đầu, không phải thay đổi."
        )
    out.append("")

    # 3
    out.append("## 3. Tính năng mới")
    out.append("")
    out.append("Toàn bộ FR trong candidate baseline; Must/Should và mốc nằm tại từng nguồn.")
    out.append("")
    for art in frs:
        out.append(render_artifact(art))

    # 4
    out.append("## 4. Thay đổi hành vi hiện có")
    out.append("")
    if chg.get("supersedes"):
        out.append(
            "Không có FR nào bump revision: mọi FR trong baseline này mang key mới. "
            f"FR của `{chg['supersedes']}` đã deprecated; ánh xạ cũ sang mới ở PRD mục IV.3."
        )
    else:
        out.append(
            "Không có baseline sản phẩm đã approved để so diff."
        )
    out.append("")

    # 5
    out.append("## 5. NGOÀI phạm vi lần này")
    out.append("")
    scope_out = ""
    if prd:
        scope_out = section(
            rebase_links(body_after_frontmatter(read_bytes(REPO / prd["path"])), prd["path"]),
            "2. Ngoài phạm vi",
        )
    out.append(scope_out if scope_out else "Xem PRD mục IV.2.")
    out.append("")
    on_disk = {p.stem for p in (AIDE / "requirements" / "fr").glob("FR-*.md")}
    missing = sorted(on_disk - {a["key"] for a in frs})
    out.append(
        "Không có FR chuẩn tắc nào bị giấu khỏi candidate."
        if not missing
        else "FR có trên đĩa nhưng chưa vào baseline: " + ", ".join(missing) + "."
    )
    out.append("")

    # 6
    out.append("## 6. Ràng buộc mới")
    out.append("")
    for art in nfrs:
        out.append(render_artifact(art))

    # 7
    out.append("## 7. Câu hỏi mở còn lại")
    out.append("")
    out.append(render_open_questions(chg_dir))

    VIEWS.mkdir(parents=True, exist_ok=True)
    target = VIEWS / f"{view_key}.md"
    target.write_bytes("\n".join(out).encode("utf-8"))
    return target


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("render", "check"):
        p = sub.add_parser(name)
        p.add_argument("--baseline", required=True, help="tên file trong baseline/, ví dụ BL-r9.yaml")
        p.add_argument("--change-set", help="key Change Set; bắt buộc khi có nhiều Change Set")
        if name == "render":
            p.add_argument("--recovery", action="store_true",
                           help="recovery review: ghi view ra file riêng theo baseline")
    args = ap.parse_args(argv)

    try:
        baseline_path = pick_change_set(args.change_set) / "baseline" / args.baseline
        if args.cmd == "check":
            baseline = parse_baseline(baseline_path)
            issues = verify(baseline)
            print(f"Baseline: {baseline['head'].get('key', args.baseline)}")
            print(f"Artifact: {len(baseline['artifacts'])}")
            if issues:
                print(f"\n{len(issues)} lệch:")
                for i in issues:
                    print(f"  - {i}")
                return 1
            print("Hash, revision, key và UID: khớp toàn bộ.")
            return 0

        target = render(args.baseline, args.change_set, args.recovery)
        print(f"Đã ghi {rel(target)}")
        return 0
    except Problem as exc:
        print(f"LỖI: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
