"""Build an HTML page that draws the 8 hand-written oracle diagrams (Mermaid) with their evidence."""
import html
import json
import re
from pathlib import Path

ROOT = Path(r"D:/GitLab-Project/VSF-L3 Generator")
ORACLE = ROOT / "experiments/quote-evidence/oracle"
OUT = Path(__file__).with_name("oracle-diagrams.html")

REPOS = [  # (file, short name, group)
    ("rhoboro-async-fastapi-sqlalchemy.json", "rhoboro", "kiểm"),
    ("teamhide-fastapi-boilerplate.json", "teamhide", "kiểm"),
    ("fastapi-boilerplate.json", "boilerplate", "kiểm"),
    ("lnbits.json", "lnbits", "kiểm"),
    ("fastapi-best-architecture.json", "fba", "kiểm"),
    ("full-stack-fastapi-template.json", "fullstack", "chỉnh"),
    ("fastapi-realworld.json", "realworld", "chỉnh"),
    ("kibo-backend.json", "kibo", "chỉnh"),
]


def clean(text: str) -> str:
    """No em/en dashes on the page."""
    return text.replace("—", "-").replace("–", "-")


def node_id(key: str) -> str:
    return "n_" + re.sub(r"\W", "_", key)


def members(o: dict) -> dict[str, list[str]]:
    """Files of each component, from the repository on disk (a path in the oracle is a member list, not a sample)."""
    import sys
    sys.path.insert(0, str(ROOT / "experiments/quote-evidence"))
    import evaluate, graph, inventory, pyindex
    repo = ROOT / o["local_dir"]
    idx = pyindex.index(repo, inventory.scan(repo))
    out = {k: [] for k in o["components"]}
    for f in graph.content_files(idx):
        k = evaluate.oracle_owner(o, f)
        if k:
            out[k].append(f)
    return out


def label(key: str, files: list[str]) -> str:
    dirs = sorted({str(Path(f).parent).replace("\\", "/") for f in files})
    common = dirs[0] if len(dirs) == 1 else ""
    if len(dirs) > 1:
        parts = [d.split("/") for d in dirs]
        n = 0
        while all(len(x) > n for x in parts) and len({x[n] for x in parts}) == 1:
            n += 1
        common = "/".join(parts[0][:n]) + "/*" if n else "nhiều thư mục"
    where = "" if common in ("", ".") else f" · {common}"
    return f"<b>{key}</b><br/><small>{len(files)} file{where}</small>"


LAYERS = [("entry", "Điểm vào"), ("api", "API"), ("service", "Nghiệp vụ"), ("data", "Dữ liệu"), ("infra", "Hạ tầng")]
LAYER_NAME = dict(LAYERS)
NOT_DRAWN = [  # labelled `acceptable` edges: real, listed under the diagram, not drawn
    ("wiring", "Lắp ráp", "Cạnh lắp ráp, có thật nhưng không vẽ"),
    ("pass", "Chỉ truyền", "Cạnh chỉ nhận hoặc tự mở session, client rồi truyền đi, không vẽ"),
    ("check", "Kiểm tra", "Cạnh kiểm tra rồi quay về (token, quyền, session), không vẽ"),
    ("up", "Đi lên", "Cạnh đi ngược lên tầng trên, không vẽ"),
]


def mermaid(o: dict, files: dict) -> str:
    comps, exts = o["components"], o["externals"]
    req = o["required"]
    used = {r[0] for r in req} | {r[1] for r in req}
    shared = set(o.get("shared", []))
    layers = o.get("layers")
    node = lambda key: f'{node_id(key)}["{label(key, files[key])}"]'
    ext_keys = [k for k in exts if f"ext:{k}" in used]
    direction = "TB" if layers or len(comps) > 10 else "LR"
    lines = [f"flowchart {direction}"]
    if layers:  # rev 3: one frame per layer, top to bottom; a block with no flow edge gets a dashed border
        frames = []
        for layer, title in LAYERS:
            keys = [k for k in comps if k not in shared and layers.get(k, [None])[0] == layer]
            if keys:
                frames.append(f"L_{layer}")
                lines.append(f'  subgraph L_{layer}["{title}"]')
                lines += [f"    {node(k)}" + ("" if k in used else ":::idle") for k in keys]
                lines.append("  end")
        if ext_keys:
            frames.append("L_ext")
            lines.append('  subgraph L_ext["Hệ thống ngoài"]')
            lines += [f'    {node_id("ext_" + k)}[("{k}")]' for k in ext_keys]
            lines.append("  end")
        lines += [f"  {a} ~~~ {b}" for a, b in zip(frames, frames[1:])]  # keeps the frames in layer order
        lines.append("  classDef idle stroke-dasharray: 4 3")
        groups = [("Dùng chung (không vẽ cạnh)", "shared", [k for k in comps if k in shared])]
    else:
        lines += [f"  {node(k)}" for k in comps if k in used]
        lines += [f'  {node_id("ext_" + k)}[("{k}")]' for k in ext_keys]
        groups = [("Dùng chung (không vẽ cạnh)", "shared", [k for k in comps if k in shared]),
                  ("Không có cạnh luồng (chỉ lắp ráp hoặc chỉ nối ra ngoài)", "idle",
                   [k for k in comps if k not in used and k not in shared])]
    for title, group, keys in groups:
        if keys:
            lines.append(f'  subgraph {group}["{title}"]')
            lines += [f"    {node(k)}" for k in keys]
            lines.append("  end")
    for r in req:
        a, b = r[0], r[1]
        note = r[2] if len(r) > 2 else ""
        src = node_id(a)
        dst = node_id("ext_" + b[4:]) if b.startswith("ext:") else node_id(b)
        arrow = "==>" if "không qua import" in note else "-->"
        lines.append(f"  {src} {arrow} {dst}")
    return "\n".join(lines)


def section(fname: str, name: str, group: str) -> str:
    o = json.loads((ORACLE / fname).read_text(encoding="utf-8"))
    files = members(o)
    comps, exts, req = o["components"], o["externals"], o["required"]
    layers = o.get("layers", {})
    labelled = {tag: [a for a in o.get("acceptable", []) if len(a) > 2 and a[2] == tag] for tag, *_ in NOT_DRAWN}
    shown = [row for row in NOT_DRAWN if row[0] == "wiring" or layers]  # rev 2 oracles have only wiring
    acc = [a for a in o.get("acceptable", []) if not (len(a) > 2 and a[2] in labelled)]
    no_import = sum("không qua import" in (r[2] if len(r) > 2 else "") for r in req)
    note = f'<p class="note">{html.escape(clean(o["note"]))}</p>' if o.get("note") else ""

    def layer_cell(k: str) -> str:
        if k in o.get("shared", []):
            return "<td>dùng chung</td>"
        if k not in layers:
            return "<td>-</td>"
        name, proof = layers[k][0], layers[k][1] if len(layers[k]) > 1 else ""
        return f"<td>{LAYER_NAME.get(name, name)}<br><small>{html.escape(clean(proof))}</small></td>"

    comp_rows = "".join(
        f"<tr><th scope=row>{html.escape(k)}</th>{layer_cell(k) if layers else ''}<td class=num>{len(files[k])}</td>"
        f"<td>{'<br>'.join(f'<code>{html.escape(p)}</code>' for p in v)}</td></tr>"
        for k, v in comps.items())
    edge_rows = lambda rows: "".join(
        f"<tr><td><code>{html.escape(a[0])}</code></td><td><code>{html.escape(a[1])}</code></td>"
        f"<td>{html.escape(clean(a[3])) if len(a) > 3 else ''}</td></tr>" for a in rows)
    not_drawn_counts = "".join(f"<div><dt>{short} (không vẽ)</dt><dd>{len(labelled[tag])}</dd></div>"
                               for tag, short, _ in shown)
    not_drawn_blocks = "".join(
        f'<details class="acc"><summary>{title} ({len(labelled[tag])})</summary>'
        f'<div class="scroll"><table><tbody>{edge_rows(labelled[tag])}</tbody></table></div></details>'
        for tag, _, title in shown)
    req_rows = "".join(
        f"<tr><td><code>{html.escape(r[0])}</code></td><td><code>{html.escape(r[1])}</code></td>"
        f"<td>{html.escape(clean(r[2])) if len(r) > 2 else ''}</td></tr>" for r in req)
    acc_items = ", ".join(f"<code>{html.escape(a[0])} → {html.escape(a[1])}</code>" for a in acc) or "không có"
    ext_items = " ".join(f'<span class="chip">{html.escape(k)}</span>' for k in exts)
    return f"""
<section id="{name}" class="repo">
  <header class="repo-head">
    <div>
      <h2>{html.escape(o['repo'])}</h2>
      <p class="meta"><span class="group group-{'test' if group == 'kiểm' else 'tune'}">Nhóm {group}</span>
        <span>Bản {o.get('rev', '')}</span> <code>{html.escape(o.get('source', ''))[:21]}</code>
        · viết {html.escape(clean(o.get('written', '')))}</p>
    </div>
    <dl class="counts">
      <div><dt>Khối</dt><dd>{len(comps)}</dd></div>
      <div><dt>Dùng chung</dt><dd>{len(o.get('shared', []))}</dd></div>
      <div><dt>Hệ thống ngoài</dt><dd>{len(exts)}</dd></div>
      <div><dt>Cạnh luồng</dt><dd>{len(req)}</dd></div>
      {not_drawn_counts}
      <div><dt>Không qua import</dt><dd>{no_import}</dd></div>
      <div><dt>Chấp nhận được</dt><dd>{len(acc)}</dd></div>
    </dl>
  </header>
  {note}
  <div class="diagram"><pre class="mermaid">
{html.escape(mermaid(o, files))}
  </pre></div>
  <p class="exts">Hệ thống ngoài: {ext_items}</p>
  <div class="split">
    <details open><summary>Cạnh bắt buộc và bằng chứng ({len(req)})</summary>
      <div class="scroll"><table><thead><tr><th>Từ</th><th>Tới</th><th>Bằng chứng trong code</th></tr></thead>
      <tbody>{req_rows}</tbody></table></div></details>
    <details><summary>Khối và thành viên ({len(comps)})</summary>
      <p class="hint">Đường dẫn là danh sách thành viên: thư mục nghĩa là mọi file trong đó. Cột số là số file có nội dung.</p>
      <div class="scroll"><table><tbody>{comp_rows}</tbody></table></div></details>
  </div>
  {not_drawn_blocks}
  <details class="acc"><summary>Cạnh "chấp nhận được" ({len(acc)}): vẽ ra không bị trừ điểm P thường, bị tính sai ở P khắt khe</summary>
    <p class="acc-list">{acc_items}</p></details>
</section>"""


def rescore_rows() -> str:
    """Existing runs scored against rev 1 and rev 2 (internal edges)."""
    import sys
    sys.path.insert(0, str(ROOT / "experiments/quote-evidence"))
    import evaluate
    runs = {"rhoboro": "v4-rhoboro", "teamhide": "v3-teamhide", "boilerplate": "v3-boilerplate", "lnbits": "v5-lnbits",
            "fba": "v6-fba", "fullstack": "fullstack-r4", "realworld": "realworld-r1", "kibo": "kibo-r3"}
    f = lambda x: "-" if x is None else f"{x:.2f}".replace(".", ",")
    rows = []
    for fname, name, group in REPOS:
        g = json.loads((ROOT / "evaluation/quote-evidence/runs" / runs[name] / "graph.json").read_text(encoding="utf-8"))
        g.setdefault("file_lines", {})
        cells = []
        for folder in ("rev1", "rev2", "."):
            o = json.loads((ORACLE / folder / fname).read_text(encoding="utf-8"))
            if folder == "." and o.get("rev") != 3:
                cells.append("<td class=num>-</td>" * 3)
                continue
            s = evaluate.score(g, o)["internal"]
            cells.append(f"<td class=num>{f(s['precision'])}</td><td class=num>{f(s['precision_strict'])}</td>"
                         f"<td class=num>{f(s['recall'])}</td>")
        rows.append(f"<tr><th scope=row>{name}</th><td>{group}</td><td><code>{runs[name]}</code></td>{''.join(cells)}</tr>")
    return "".join(rows)


nav = "".join(f'<a href="#{n}">{n}<span>{g}</span></a>' for _, n, g in REPOS)
body = "".join(section(*r) for r in REPOS)
page = f"""<title>Sơ đồ đáp án 8 repo</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
:root {{
  --bg: #f6f7f9; --surface: #ffffff; --ink: #1c2230; --muted: #5b6475; --line: #dde1e8;
  --accent: #2f54c9; --accent-soft: #e6ecfb; --test: #1f7a55; --test-soft: #e3f3ec; --tune: #8a5a12; --tune-soft: #f7eedd;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    color-scheme: dark;
    --bg: #11151c; --surface: #171c25; --ink: #e5e8ef; --muted: #9aa3b5; --line: #2a3140;
    --accent: #8fa8f5; --accent-soft: #1e2944; --test: #6fcf9f; --test-soft: #16322a; --tune: #e6b865; --tune-soft: #352912;
  }}
}}
:root[data-theme="dark"] {{
  color-scheme: dark;
  --bg: #11151c; --surface: #171c25; --ink: #e5e8ef; --muted: #9aa3b5; --line: #2a3140;
  --accent: #8fa8f5; --accent-soft: #1e2944; --test: #6fcf9f; --test-soft: #16322a; --tune: #e6b865; --tune-soft: #352912;
}}
* {{ box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--ink); font: 15px/1.6 "Be Vietnam Pro", system-ui, sans-serif; }}
code, .mono {{ font-family: "JetBrains Mono", ui-monospace, monospace; font-size: .86em; }}
.wrap {{ max-width: 1180px; margin: 0 auto; padding-inline: 20px; padding-block: 28px 64px; }}
h1 {{ font-size: clamp(1.6rem, 3vw, 2.2rem); line-height: 1.2; margin: 0 0 8px; text-wrap: balance; letter-spacing: -.01em; }}
.lede {{ color: var(--muted); max-width: 70ch; margin: 0; }}
.guide {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px 32px; margin: 24px 0 8px;
  padding: 20px 0; border-block: 1px solid var(--line); }}
.guide h3 {{ font-size: .95rem; margin: 0 0 6px; }}
.guide p, .guide li {{ color: var(--muted); font-size: .92rem; margin: 0; }}
.guide ul {{ margin: 0; padding-left: 18px; }}
.legend {{ display: grid; gap: 6px; }}
.legend div {{ display: flex; gap: 10px; align-items: center; font-size: .92rem; color: var(--muted); }}
.legend svg {{ flex: none; }}
nav {{ position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--bg); display: flex; flex-wrap: wrap;
  gap: 6px; padding-block: 12px; border-bottom: 1px solid var(--line); }}
nav a {{ text-decoration: none; color: var(--ink); background: var(--surface); border: 1px solid var(--line);
  padding: 4px 10px; border-radius: 8px; font-weight: 500; font-size: .9rem; display: inline-flex; gap: 6px; align-items: baseline; }}
nav a span {{ color: var(--muted); font-weight: 400; font-size: .78rem; }}
nav a:hover, nav a:focus-visible {{ border-color: var(--accent); outline: none; }}
.repo {{ padding-block: 36px 8px; scroll-margin-top: 64px; }}
.repo-head {{ display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px; align-items: end; }}
.repo h2 {{ font-size: 1.35rem; margin: 0; }}
.meta {{ margin: 4px 0 0; color: var(--muted); font-size: .88rem; display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }}
.group {{ font-weight: 600; font-size: .78rem; padding: 1px 8px; border-radius: 8px; }}
.group-test {{ color: var(--test); background: var(--test-soft); }}
.group-tune {{ color: var(--tune); background: var(--tune-soft); }}
.counts {{ display: flex; flex-wrap: wrap; gap: 18px; margin: 0; }}
.counts div {{ display: grid; }}
.counts dt {{ color: var(--muted); font-size: .76rem; }}
.counts dd {{ margin: 0; font-size: 1.25rem; font-weight: 600; font-variant-numeric: tabular-nums; }}
.note {{ color: var(--muted); font-size: .92rem; max-width: 80ch; margin: 10px 0 0; }}
.diagram {{ margin-top: 16px; background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 16px;
  overflow-x: auto; }}
.diagram pre {{ margin: 0; min-width: 640px; }}
.exts {{ margin: 10px 0 0; font-size: .9rem; color: var(--muted); display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }}
.chip {{ background: var(--accent-soft); color: var(--accent); padding: 0 8px; border-radius: 8px; font-size: .84rem; }}
.split {{ display: grid; grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr); gap: 16px; margin-top: 16px; }}
@media (max-width: 860px) {{ .split {{ grid-template-columns: 1fr; }} }}
details {{ background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 10px 14px; }}
summary {{ cursor: pointer; font-weight: 600; font-size: .93rem; }}
summary:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
.scroll {{ overflow-x: auto; max-height: 460px; overflow-y: auto; margin-top: 8px; }}
table {{ border-collapse: collapse; width: 100%; font-size: .88rem; }}
th, td {{ text-align: left; vertical-align: top; padding: 6px 8px; }}
thead th {{ color: var(--muted); font-weight: 500; font-size: .8rem; position: sticky; top: 0; background: var(--surface); }}
tbody tr + tr {{ border-top: 1px solid var(--line); }}
tbody th {{ font-weight: 600; white-space: nowrap; }}
.acc {{ margin-top: 12px; }}
.acc summary {{ font-weight: 500; color: var(--muted); }}
.standard {{ padding-block: 8px 20px; }}
.standard h2 {{ font-size: 1.2rem; margin: 8px 0; }}
.standard h3 {{ font-size: 1rem; margin: 20px 0 4px; }}
.standard ol {{ margin: 0; padding-left: 20px; max-width: 90ch; color: var(--muted); }}
.standard li + li {{ margin-top: 4px; }}
.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
.hint {{ color: var(--muted); font-size: .84rem; margin: 6px 0 0; }}
.acc-list {{ font-size: .86rem; line-height: 2; margin: 8px 0 0; }}
</style>

<div class="wrap">
  <h1>Sơ đồ đáp án dùng để chấm P và R</h1>
  <p class="lede">Đáp án đang nâng từ bản 2 lên bản 3 (28/09/2026). Bản 3 xếp mỗi khối vào một tầng, chỉ vẽ cạnh đi xuống, và bỏ cạnh chỉ truyền session hoặc chỉ kiểm tra rồi quay về. Repo chưa nâng thì vẽ như bản 2. Bản cũ giữ ở <code>oracle/rev1/</code>, <code>oracle/rev2/</code>.
  Sơ đồ chỉ vẽ luồng xử lý (request, tác vụ nền, lệnh CLI). Cạnh lắp ráp (container DI, khởi động, tắt) có thật nhưng không vẽ, liệt kê riêng dưới mỗi sơ đồ. Nhãn khối ghi số file, không phải một file đại diện.</p>

  <div class="guide">
    <div class="legend">
      <h3>Cách đọc sơ đồ</h3>
      <div><svg width="46" height="10" aria-hidden="true"><line x1="0" y1="5" x2="38" y2="5" stroke="currentColor" stroke-width="1.5"/><path d="M38 1 L46 5 L38 9 Z" fill="currentColor"/></svg>Cạnh bắt buộc, có import chứng minh</div>
      <div><svg width="46" height="10" aria-hidden="true"><line x1="0" y1="5" x2="38" y2="5" stroke="currentColor" stroke-width="4"/><path d="M38 0 L46 5 L38 10 Z" fill="currentColor"/></svg>Cạnh bắt buộc không qua import (pipeline chỉ dựa import sẽ không thấy)</div>
      <p>Hình trụ là hệ thống ngoài (cơ sở dữ liệu, Redis, SMTP...). Khung \"Dùng chung\" gồm cấu hình, log, lỗi, hằng số, helper: sơ đồ không vẽ cạnh tới chúng.</p>
      <p>Bản 3: khung là tầng, từ trên xuống: Điểm vào, API, Nghiệp vụ, Dữ liệu, Hạ tầng, Hệ thống ngoài. Khối viền nét đứt không có cạnh luồng.</p>
    </div>
    <div>
      <h3>Cách chấm</h3>
      <ul>
        <li>Mỗi khối AI tạo ra được coi là khối đáp án có nhiều file chung nhất với nó.</li>
        <li>Cạnh AI vẽ trùng cạnh bắt buộc là <b>đúng</b>; trùng cạnh "chấp nhận được" thì <b>không tính</b>; còn lại là <b>sai</b>.</li>
        <li>P = đúng / (đúng + sai). P khắt khe tính cả cạnh "chấp nhận được" là sai. R = đúng / số cạnh bắt buộc.</li>
        <li>Tiêu chí đạt: P ≥ 0,8, R ≥ 0,6, trích dẫn hợp lệ ≥ 90%.</li>
      </ul>
    </div>
    <div>
      <h3>Hai nhóm repo</h3>
      <p><b>Nhóm chỉnh</b> dùng để sửa prompt và code. <b>Nhóm kiểm</b> dùng để kết luận pipeline có tái lập được trên repo lạ không. Tất cả đều là FastAPI.</p>
    </div>
  </div>

  <section class="standard">
    <h2>Chuẩn đáp án bản 3</h2>
    <ol>
      <li>Giữ luồng chính (route, service, truy cập dữ liệu, DB và hệ thống ngoài) và cả luồng phụ (CLI, trang admin, worker, plugin). Chỉ bỏ phần không thuộc luồng nào, ví dụ file không ai dùng. Chỉ vẽ cạnh luồng xử lý; cạnh lắp ráp ghi riêng với nhãn wiring.</li>
      <li>Khối không cần trùng thư mục. Gộp khối cùng tầng, cùng cơ chế: 6 plugin nạp chung một vòng lặp là một khối; application và domain của một tính năng là một khối service; crud và models là một khối dữ liệu.</li>
      <li>Khối dùng chung ghi rõ trong trường <code>shared</code> và không có cạnh.</li>
      <li>Mỗi cạnh bắt buộc có <code>file:dòng</code>. Cạnh không qua import chỉ giữ khi thuộc luồng chính và không có đường import thay thế.</li>
      <li>Cạnh "chấp nhận được" do code sinh: mọi cạnh import thật giữa hai khối không dùng chung mà không nằm trong danh sách bắt buộc. Cạnh tới hệ thống ngoài phụ thì ghi tay.</li>
      <li>Mỗi khối không dùng chung thuộc một tầng (Điểm vào, API, Nghiệp vụ, Dữ liệu, Hạ tầng), kèm một dòng code làm bằng chứng. Worker tác vụ nền ở tầng Nghiệp vụ.</li>
      <li>Sơ đồ chỉ đi một chiều, từ tầng trên xuống. Không vẽ: cạnh đi lên (up), cạnh chỉ nhận hoặc mở session rồi truyền đi (pass), cạnh kiểm tra token, quyền, session rồi quay về (check). Các cạnh này liệt kê dưới sơ đồ.</li>
    </ol>
    <h3>Điểm các lần chạy cũ theo các bản đáp án</h3>
    <p class="note">Cạnh nội bộ, cùng kết quả chạy, chỉ đổi đáp án. Ba repo nhóm chỉnh là lần chạy của phiên bản pipeline cũ. Cột bản 3 để trống khi repo chưa nâng.</p>
    <div class="scroll"><table class="scores"><thead><tr><th>Repo</th><th>Nhóm</th><th>Lần chạy</th>
      <th class=num>Bản 1 P</th><th class=num>Pk</th><th class=num>R</th><th class=num>Bản 2 P</th><th class=num>Pk</th><th class=num>R</th>
      <th class=num>Bản 3 P</th><th class=num>Pk</th><th class=num>R</th></tr></thead>
      <tbody>{rescore_rows()}</tbody></table></div>
  </section>

  <nav aria-label="Chọn repo">{nav}</nav>
  {body}
</div>
"""
assert "—" not in page and "–" not in page, "dash found"
OUT.write_text(page, encoding="utf-8")
print(OUT, len(page))
