"""So khớp output công cụ với ground truth, in precision/recall và từng ca lệch.

Chạy:
    python evaluation/compare.py <ground_truth.json> <IAM.json> <result.json>

Phạm vi so khớp lấy từ chính ground truth (meta.scope_dirs), không viết cứng ở đây.
"""

import json
import pathlib
import sys

SCOPE_DIRS = ()


def norm_file(p):
    return p.replace("\\", "/")


def in_scope(p):
    return norm_file(p).startswith(SCOPE_DIRS)


def norm_path(p):
    """Bỏ dấu / thừa ở cuối để '/x/' và '/x' coi là một."""
    p = p.rstrip("/")
    return p or "/"


def pr(tp, fp, fn):
    precision = tp / (tp + fp) if (tp + fp) else None
    recall = tp / (tp + fn) if (tp + fn) else None
    return precision, recall


def pct(x):
    return "—" if x is None else f"{x * 100:.1f}%"


def h1(s):
    print("\n" + "=" * 72)
    print(s)
    print("=" * 72)


def main():
    global SCOPE_DIRS
    gt_path = pathlib.Path(sys.argv[1])
    iam_path = pathlib.Path(sys.argv[2])
    out_path = pathlib.Path(sys.argv[3])
    if not iam_path.exists():
        sys.exit(f"Chưa có {iam_path}. Chạy l3gen trước.")
    gt = json.loads(gt_path.read_text(encoding="utf-8"))
    iam = json.loads(iam_path.read_text(encoding="utf-8"))
    SCOPE_DIRS = tuple(gt["meta"]["scope_dirs"])
    result = {"meta": gt["meta"]}

    print(f"\nRepo: {gt['meta']['repo']} @ {gt['meta']['commit'][:7]}")
    print(f"Phạm vi: {', '.join(SCOPE_DIRS)}")

    # Prefix cấp ứng dụng có thể là biến (vd {settings.API_V1_STR}). Nếu công cụ
    # ghi kèm biểu thức đó thì tách ra trước khi so, và đếm riêng xem nó có ghi không.
    app_expr = gt["meta"].get("app_prefix_expr")

    def strip_app_prefix(p):
        if app_expr and p.startswith(app_expr):
            return norm_path(p[len(app_expr):]) or "/"
        return p

    # ---------------------------------------------------------------- ROUTE
    h1(f"1. ROUTE — phạm vi: {', '.join(SCOPE_DIRS)}")

    # Đường dẫn trông đợi ở output.
    #   - Tiền tố cấp ứng dụng là BIẾN (template): công cụ ghi "{expr}/x"; hàm
    #     strip_app_prefix bên trên gỡ expr ra, nên trông đợi là gt["path"].
    #   - Tiền tố là CHUỖI HẰNG (dispatch, app.mount("/api/v1")): công cụ phải ghi
    #     URL thật, tức gt["path_with_mount"].
    def expected(r):
        if app_expr:
            return norm_path(r["path"])
        return norm_path(r.get("path_with_mount") or r["path"])

    gt_routes = {(r["method"], expected(r)): r for r in gt["routes"]}
    # Dạng THIẾU tiền tố mount — dùng để phân loại nguyên nhân khi có ca lệch,
    # thay vì gộp chung vào "báo thừa".
    gt_no_mount = {
        (r["method"], norm_path(r["path"])): r
        for r in gt["routes"]
        if not app_expr and r.get("path_with_mount")
    }
    tool_routes = {}
    carried_app_expr = 0
    for r in iam["routes"]:
        f = norm_file(r["location"]["file"])
        if not in_scope(f):
            continue
        p = norm_path(r["path"])
        if app_expr and p.startswith(app_expr):
            carried_app_expr += 1
        tool_routes[(r["method"], norm_path(strip_app_prefix(p)))] = r

    hit = sorted(set(gt_routes) & set(tool_routes))
    missed = sorted(set(gt_routes) - set(tool_routes))
    extra = sorted(set(tool_routes) - set(gt_routes))
    p, rc = pr(len(hit), len(extra), len(missed))

    print(f"Ground truth : {len(gt_routes)}")
    print(f"Công cụ báo  : {len(tool_routes)}")
    print(f"Khớp         : {len(hit)}   Bỏ sót: {len(missed)}   Báo thừa: {len(extra)}")
    print(f"Precision    : {pct(p)}")
    print(f"Recall       : {pct(rc)}")

    # Vị trí file:dòng có trỏ đúng chỗ không
    wrong_loc = []
    for k in hit:
        g, t = gt_routes[k], tool_routes[k]
        tf = norm_file(t["location"]["file"])
        ls, le = t["location"]["line_start"], t["location"]["line_end"]
        if tf != g["file"] or not (ls - 6 <= g["line"] <= le):
            wrong_loc.append(
                {"route": f"{k[0]} {k[1]}", "gt": f"{g['file']}:{g['line']}",
                 "tool": f"{tf}:{ls}-{le}"}
            )
    print(f"Vị trí sai   : {len(wrong_loc)} / {len(hit)} ca khớp")
    for w in wrong_loc[:10]:
        print(f"   {w['route']}\n     ground truth {w['gt']}\n     công cụ      {w['tool']}")

    if missed:
        print("\nBỏ sót:")
        for k in missed:
            g = gt_routes[k]
            print(f"   {k[0]:6} {k[1]}   ({g['file']}:{g['line']})")
    missing_mount = [k for k in extra if k in gt_no_mount]
    if missing_mount:
        print(f"\nTrong đó {len(missing_mount)} ca là route CÓ THẬT nhưng thiếu tiền tố"
              f" mount {gt['meta'].get('mount_prefix')}:")
        for k in missing_mount[:5]:
            print(f"   công cụ ghi {k[1]}   →   URL thật"
                  f" {norm_path(gt_no_mount[k]['path_with_mount'])}")
        if len(missing_mount) > 5:
            print(f"   … và {len(missing_mount) - 5} ca nữa, cùng nguyên nhân")
    if extra:
        print("\nBáo thừa:")
        for k in extra:
            t = tool_routes[k]
            note = "  [thiếu tiền tố mount]" if k in gt_no_mount else ""
            print(f"   {k[0]:6} {k[1]}   ({norm_file(t['location']['file'])}:"
                  f"{t['location']['line_start']})  {t['confidence']}/{t['completeness']}{note}")

    # Precision tách theo confidence (SPEC 8.5.2)
    by_conf = {}
    for k, t in tool_routes.items():
        c = t["confidence"]
        b = by_conf.setdefault(c, {"tp": 0, "fp": 0})
        b["tp" if k in gt_routes else "fp"] += 1
    print("\nPrecision tách theo confidence:")
    for c, b in sorted(by_conf.items()):
        pc, _ = pr(b["tp"], b["fp"], 0)
        print(f"   {c:9} n={b['tp'] + b['fp']:3}  đúng {b['tp']:3}  sai {b['fp']:3}  precision {pct(pc)}")

    comp = {}
    for t in tool_routes.values():
        comp[t["completeness"]] = comp.get(t["completeness"], 0) + 1
    print(f"Phân bố completeness: {comp}")

    # Tiền tố cấp ứng dụng: chuỗi hằng (app.mount) hay biến (prefix=settings.X)
    with_mount = None
    mount = gt["meta"].get("mount_prefix")
    if mount:
        with_mount = sum(1 for r in tool_routes.values() if norm_path(r["path"]).startswith(mount))
        verdict = ("đúng — mọi route đều có"
                   if with_mount == len(tool_routes)
                   else f"{len(tool_routes) - with_mount} route thiếu tiền tố này so với URL thật")
        print(f"\nRoute có tiền tố mount {mount}: {with_mount} / {len(tool_routes)}  → {verdict}")
    if app_expr:
        print(f"\nRoute ghi kèm biểu thức prefix {app_expr}: "
              f"{carried_app_expr} / {len(tool_routes)}")
        guessed = sum(1 for r in tool_routes.values() if norm_path(r["path"]).startswith("/api/v1"))
        print(f"Route tự đoán ra giá trị thật /api/v1: {guessed}"
              f"  (phải bằng 0 — đoán là vi phạm nguyên tắc bất biến số 3)")
        result_app_prefix = {"carried_expr": carried_app_expr, "guessed_value": guessed}
    else:
        result_app_prefix = None

    # Route đăng ký trong khối if — công cụ có nêu điều kiện không
    cond = [(k, v) for k, v in gt_routes.items() if v.get("conditional")]
    if cond:
        print("\nRoute đăng ký trong khối if:")
        for k, g in cond:
            t = tool_routes.get(k)
            if t is None:
                print(f"   {k[0]} {k[1]} — công cụ KHÔNG báo")
            else:
                print(f"   {k[0]} {k[1]} — công cụ báo, "
                      f"[{t['confidence']}/{t['completeness']}] reason={t['reason']}")
            print(f"      {g['conditional']}")

    # File lỗi cú pháp
    pe = gt["meta"].get("parse_error_expected")
    if pe:
        got = [e for e in iam.get("parse_errors", [])]
        print(f"\nFile lỗi cú pháp — chờ đợi {pe['file']}:{pe['line']} ({pe['why']})")
        print(f"   Công cụ báo {len(got)} lỗi cú pháp: "
              + ("; ".join(f"{norm_file(e.get('file', '?'))} — {e.get('error_message', '')}"
                           for e in got) if got else "(không có)"))
        result["parse_errors"] = got

    result["route"] = {
        "ground_truth": len(gt_routes), "tool_reported": len(tool_routes),
        "tp": len(hit), "fn": len(missed), "fp": len(extra),
        "precision": p, "recall": rc,
        "missed": [{"method": k[0], "path": k[1], "file": gt_routes[k]["file"],
                    "line": gt_routes[k]["line"]} for k in missed],
        "extra": [{"method": k[0], "path": k[1],
                   "file": norm_file(tool_routes[k]["location"]["file"]),
                   "line": tool_routes[k]["location"]["line_start"],
                   "confidence": tool_routes[k]["confidence"]} for k in extra],
        "wrong_location": wrong_loc,
        "precision_by_confidence": {
            c: {**b, "precision": pr(b["tp"], b["fp"], 0)[0]} for c, b in by_conf.items()},
        "completeness": comp,
        "routes_with_mount_prefix": with_mount,
        "app_prefix": result_app_prefix,
    }

    # --------------------------------------------------------------- ENTITY
    h1(f"2. BẢNG DỮ LIỆU — phạm vi: {', '.join(SCOPE_DIRS)}")

    gt_ents = {e["class_name"]: e for e in gt["entities"]}
    tool_ents = {}
    for e in iam["entities"]:
        if in_scope(norm_file(e["location"]["file"])):
            tool_ents[e["class_name"]] = e

    ehit = sorted(set(gt_ents) & set(tool_ents))
    emissed = sorted(set(gt_ents) - set(tool_ents))
    eextra = sorted(set(tool_ents) - set(gt_ents))
    ep, erc = pr(len(ehit), len(eextra), len(emissed))

    print(f"Ground truth : {len(gt_ents)}")
    print(f"Công cụ báo  : {len(tool_ents)}")
    print(f"Khớp         : {len(ehit)}   Bỏ sót: {len(emissed)}   Báo thừa: {len(eextra)}")
    print(f"Precision    : {pct(ep)}")
    print(f"Recall       : {pct(erc)}")
    if emissed:
        print("Bỏ sót:", ", ".join(emissed))
    if eextra:
        print("Báo thừa:")
        for c in eextra:
            t = tool_ents[c]
            print(f"   {c}  ({norm_file(t['location']['file'])}:{t['location']['line_start']})")

    # Ba kết cục khác nhau, không được gộp: đọc đúng / đọc sai / nói thẳng là
    # không đọc được. "Không biết" là kết quả ĐÚNG khi tên bảng sinh lúc chạy —
    # gộp nó vào "sai" là trừ điểm công cụ vì nó trung thực.
    print("\nTên bảng (chỉ xét ca khớp):")
    tbl_ok, tbl_bad, tbl_unknown = [], [], []
    for c in ehit:
        g, t = gt_ents[c], tool_ents[c]
        row = {"class": c, "ground_truth": g["table_name"], "tool": t["table_name"],
               "confidence": t["confidence"], "completeness": t["completeness"],
               "reason": t["reason"]}
        if t["table_name"] is None:
            tbl_unknown.append(row)
        elif g["table_name"] == t["table_name"]:
            tbl_ok.append(row)
        else:
            tbl_bad.append(row)
    print(f"   Đọc đúng            : {len(tbl_ok)} / {len(ehit)}")
    print(f"   Đọc SAI             : {len(tbl_bad)} / {len(ehit)}")
    print(f"   Ghi 'không đọc được': {len(tbl_unknown)} / {len(ehit)}")
    for r in tbl_bad:
        print(f"   SAI  {r['class']:18} thật '{r['ground_truth']}'  công cụ '{r['tool']}'"
              f"   [{r['confidence']}/{r['completeness']}]")
    if tbl_unknown:
        print(f"   Lý do công cụ tự ghi: {tbl_unknown[0]['reason']}")
        print("   → Tên thật của các lớp này là: "
              + ", ".join(f"{r['class']}={r['ground_truth']}" for r in tbl_unknown[:4])
              + (" …" if len(tbl_unknown) > 4 else ""))

    print("\nSố cột đọc được (ca khớp):")
    for c in ehit:
        t = tool_ents[c]
        npk = sum(1 for col in t["columns"] if col["is_primary_key"])
        nfk = sum(1 for col in t["columns"] if col["foreign_key_ref"])
        print(f"   {c:18} {len(t['columns']):3} cột, {npk} khoá chính, {nfk} khoá ngoại")

    result["entity"] = {
        "ground_truth": len(gt_ents), "tool_reported": len(tool_ents),
        "tp": len(ehit), "fn": len(emissed), "fp": len(eextra),
        "precision": ep, "recall": erc,
        "missed": emissed,
        "extra": [{"class": c, "file": norm_file(tool_ents[c]["location"]["file"]),
                   "line": tool_ents[c]["location"]["line_start"]} for c in eextra],
        "table_name_correct": len(tbl_ok),
        "table_name_wrong": tbl_bad,
        "table_name_unknown": [r["class"] for r in tbl_unknown],
    }

    # -------------------------------------------------------- EXTERNAL CALL
    h1(f"3. LỜI GỌI RA NGOÀI — phạm vi: {gt['meta']['pham_vi_external_call']}")

    tool_ext = [e for e in iam["external_calls"]]
    matched_gt, matched_tool = set(), set()
    for gi, g in enumerate(gt["external_calls"]):
        for ti, t in enumerate(tool_ext):
            if ti in matched_tool:
                continue
            loc = t["location"]
            if norm_file(loc["file"]) == g["file"] and loc["line_start"] <= g["line"] <= loc["line_end"]:
                matched_gt.add(gi)
                matched_tool.add(ti)
                break

    xmissed = [g for i, g in enumerate(gt["external_calls"]) if i not in matched_gt]
    xextra = [t for i, t in enumerate(tool_ext) if i not in matched_tool]

    # Tách "báo thừa" làm hai loại. Không gộp chung: một bên là bịa ra thứ không
    # có, một bên là tìm được lời gọi HTTP thật nhưng nằm ngoài danh sách dạng mà
    # SPEC mục 6c.3 liệt kê. Gộp lại sẽ trừ điểm công cụ vì nó làm tốt hơn spec.
    def is_borderline(t):
        return any(norm_file(t["location"]["file"]) == b["file"]
                   and t["location"]["line_start"] <= b["line"] <= t["location"]["line_end"]
                   for b in gt["external_calls_borderline"])

    x_borderline = [t for t in xextra if is_borderline(t)]
    x_fp = [t for t in xextra if not is_borderline(t)]

    xp, xrc = pr(len(matched_gt), len(xextra), len(xmissed))          # nghiêm ngặt
    xp_real, _ = pr(len(matched_gt) + len(x_borderline), len(x_fp), 0)  # tính ca ranh giới là đúng

    print(f"Ground truth : {len(gt['external_calls'])} (+{len(gt['external_calls_borderline'])} ca ranh giới)")
    print(f"Công cụ báo  : {len(tool_ext)}")
    print(f"Khớp         : {len(matched_gt)}   Bỏ sót: {len(xmissed)}")
    print(f"Ngoài GT     : {len(xextra)}  =  {len(x_fp)} bịa  +  {len(x_borderline)} ca ranh giới có thật")
    print(f"Recall       : {pct(xrc)}")
    print(f"Precision (nghiêm ngặt, coi ca ranh giới là sai) : {pct(xp)}")
    print(f"Precision (đếm 'có phải lời gọi HTTP thật không') : {pct(xp_real)}")
    if xmissed:
        print("\nBỏ sót:")
        for g in xmissed:
            print(f"   {g['file']}:{g['line']}  {g['http_method']}  {g['url_in_code']}")
            if g["note"]:
                print(f"      ghi chú ground truth: {g['note']}")
    if x_fp:
        print("\nBáo thừa thật sự (không phải lời gọi HTTP):")
        for t in x_fp:
            print(f"   {norm_file(t['location']['file'])}:{t['location']['line_start']}  "
                  f"{t['http_method']}  {t['url_or_host']}")
    else:
        print("\nKhông có ca nào công cụ báo ra mà không phải lời gọi HTTP thật.")

    print("\nCác bẫy báo thừa đã cài — công cụ có mắc không:")
    for trap in gt["false_positive_traps"]:
        mắc = any(norm_file(t["location"]["file"]) == trap["file"]
                  and t["location"]["line_start"] <= trap["line"] <= t["location"]["line_end"]
                  for t in tool_ext)
        print(f"   [{'MẮC BẪY' if mắc else 'tránh được'}] {trap['file']}:{trap['line']}")
        print(f"      {trap['why']}")

    print("\nCa ranh giới (không tính vào chỉ số):")
    for b in gt["external_calls_borderline"]:
        báo = any(norm_file(t["location"]["file"]) == b["file"]
                  and t["location"]["line_start"] <= b["line"] <= t["location"]["line_end"]
                  for t in tool_ext)
        print(f"   [{'công cụ CÓ báo' if báo else 'công cụ không báo'}] {b['file']}:{b['line']}")
        print(f"      {b['note']}")

    # Cờ try/except và URL có khớp không
    flag_bad, url_bad = [], []
    for gi in sorted(matched_gt):
        g = gt["external_calls"][gi]
        t = next(t for t in tool_ext
                 if norm_file(t["location"]["file"]) == g["file"]
                 and t["location"]["line_start"] <= g["line"] <= t["location"]["line_end"])
        if t["inside_try_except"] != g["inside_try_except"]:
            flag_bad.append({"at": f"{g['file']}:{g['line']}",
                             "gt": g["inside_try_except"], "tool": t["inside_try_except"]})
        if t["http_method"] != g["http_method"]:
            url_bad.append({"at": f"{g['file']}:{g['line']}",
                            "gt": g["http_method"], "tool": t["http_method"]})
    print(f"\nCờ try/except sai : {len(flag_bad)} / {len(matched_gt)}")
    for f in flag_bad:
        print(f"   {f['at']}  ground truth {f['gt']}  công cụ {f['tool']}")
    print(f"HTTP method sai   : {len(url_bad)} / {len(matched_gt)}")
    for f in url_bad:
        print(f"   {f['at']}  ground truth {f['gt']}  công cụ {f['tool']}")

    xconf = {}
    for t in tool_ext:
        xconf[t["confidence"]] = xconf.get(t["confidence"], 0) + 1
    xcomp = {}
    for t in tool_ext:
        xcomp[t["completeness"]] = xcomp.get(t["completeness"], 0) + 1
    print(f"\nPhân bố confidence: {xconf}")
    print(f"Phân bố completeness: {xcomp}")

    result["external_call"] = {
        "ground_truth": len(gt["external_calls"]), "tool_reported": len(tool_ext),
        "tp": len(matched_gt), "fn": len(xmissed), "fp": len(xextra),
        "fp_bia": len(x_fp), "fp_borderline": len(x_borderline),
        "precision": xp, "precision_real_call": xp_real, "recall": xrc,
        "missed": [{"file": g["file"], "line": g["line"], "method": g["http_method"],
                    "url": g["url_in_code"], "note": g["note"]} for g in xmissed],
        "extra": [{"file": norm_file(t["location"]["file"]),
                   "line": t["location"]["line_start"], "url": t["url_or_host"]} for t in xextra],
        "try_except_flag_wrong": flag_bad,
        "http_method_wrong": url_bad,
        "confidence": xconf, "completeness": xcomp,
    }

    # -------------------------------------------------------------- NGƯỠNG
    h1("4. ĐỐI CHIẾU NGƯỠNG (SPEC mục 8.5.3 — đặt trước khi chạy)")
    exact_p = result["route"]["precision_by_confidence"].get("exact", {}).get("precision")
    checks = [
        ("Route — recall", rc, 0.85),
        ("Route — precision nhóm exact", exact_p, 0.95),
        ("Bảng dữ liệu — recall", erc, 0.90),
        ("Gọi ra ngoài — recall", xrc, 0.80),
    ]
    print(f"{'Nhóm':34} {'Đo được':>9} {'Ngưỡng':>8}  Kết quả")
    allpass = True
    for name, val, thr in checks:
        ok = val is not None and val >= thr
        allpass &= ok
        print(f"{name:34} {pct(val):>9} {pct(thr):>8}  {'ĐẠT' if ok else 'KHÔNG ĐẠT'}")
    result["thresholds"] = {
        "all_pass": allpass,
        "checks": [{"name": n, "measured": v, "threshold": t,
                    "pass": v is not None and v >= t} for n, v, t in checks],
    }

    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nĐã ghi {out_path}")


if __name__ == "__main__":
    main()
