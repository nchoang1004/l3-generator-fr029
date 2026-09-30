"""Code tự gắn bằng chứng cho khối đáp án được bao nhiêu, không cần AI trích dẫn. Không gọi AI.

    python code_evidence.py [--detail]

Mỗi khối không dùng chung của đáp án, xét file của chính khối, xếp vào loại đầu tiên khớp:
  chắc  = một file có dấu hiệu chắc (flow.analyze "sure") đúng tầng khối;
  io    = một file có dòng mở kết nối ra ngoài;
  gọi   = một file ngoài khối (không dùng chung) gọi vào file của khối, loại cạnh flow (dòng ở file gọi);
  không = không có dòng nào ở trên.
Cột "io Hạ tầng": khối loại io có tầng infra (dòng mở kết nối chứng minh đúng tầng). Cột "gọi từ trên": khối loại
gọi có file gọi thuộc khối tầng cao hơn (chứng minh khối nằm dưới trong luồng, chưa chứng minh tầng).
Cột "trùng đáp án": dòng bằng chứng tầng mà đáp án chọn nằm trong các dòng code tìm được (chắc, io, gọi).
--detail in khối "không" và khối lệch, chỉ cho repo lộ (repo kín chỉ số tổng).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
Q = ROOT / "experiments/quote-evidence"
sys.path.insert(0, str(Q))
import calls, evaluate, flow, graph, inventory, pyindex  # noqa: E402

REPOS = [("rhoboro", "rhoboro-async-fastapi-sqlalchemy", True), ("fullstack", "full-stack-fastapi-template", True),
         ("realworld", "fastapi-realworld", True), ("teamhide", "teamhide-fastapi-boilerplate", True),
         ("boilerplate", "fastapi-boilerplate", False), ("kibo", "kibo-backend", False),
         ("lnbits", "lnbits", False), ("fba", "fastapi-best-architecture", False)]
KINDS = ("chắc", "io", "gọi", "không")

print("| Repo | Lộ | Khối | chắc | io | gọi | không | io Hạ tầng | gọi từ trên | Trùng dòng đáp án |")
print("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
total = {True: [0] * 8, False: [0] * 8}
LAYERS = ("entry", "api", "service", "data", "infra")
for name, orc, exposed in REPOS:
    oracle = json.loads((Q / "oracle" / f"{orc}.json").read_text(encoding="utf-8"))
    repo = ROOT / oracle["local_dir"]
    idx = pyindex.index(repo, inventory.scan(repo))
    an = flow.analyze(idx, calls.facts(idx))
    owner = {p: evaluate.oracle_owner(oracle, p) for p in graph.content_files(idx)}
    shared = set(oracle["shared"])
    count, same, detail, io_infra, from_above = dict.fromkeys(KINDS, 0), 0, [], 0, 0
    for key, (layer, quote) in sorted(oracle["layers"].items()):
        if key in shared:
            continue
        mine = {p for p, k in owner.items() if k == key}
        sure = {(p, an["sure"][p][1]) for p in mine if p in an["sure"] and an["sure"][p][0] == layer}
        io = {(p, line) for p in mine for line in an["io"].get(p, {}).values()}
        into = {(a, line) for (a, b), (kind, line) in an["pairs"].items()
                if b in mine and a not in mine and owner.get(a) not in shared and owner.get(a) and kind == "flow"}
        kind = "chắc" if sure else "io" if io else "gọi" if into else "không"
        count[kind] += 1
        io_infra += kind == "io" and layer == "infra"
        above = [oracle["layers"][owner[a]][0] for a, _ in into if owner[a] in oracle["layers"]]
        from_above += kind == "gọi" and any(LAYERS.index(t) < LAYERS.index(layer) for t in above)
        f, rest = quote.split(":", 1)
        hit = (f, int(rest.split(" ", 1)[0])) in sure | io | into
        same += hit
        if kind == "không" or not hit:
            detail.append(f"    {key} ({layer}): {kind}, trùng đáp án {'có' if hit else 'không'}; đáp án {quote[:90]}")
    n = sum(count.values())
    row = [n] + [count[k] for k in KINDS] + [io_infra, from_above, same]
    total[exposed] = [a + b for a, b in zip(total[exposed], row)]
    print(f"| {name} | {'lộ' if exposed else 'kín'} | " + " | ".join(map(str, row)) + " |")
    if "--detail" in sys.argv and exposed:
        print("\n".join(detail))
for exposed in (True, False):
    t = total[exposed]
    print(f"\nTổng repo {'lộ' if exposed else 'kín'}: {t[0]} khối; chắc {t[1]}, io {t[2]}, gọi {t[3]}, không {t[4]}; "
          f"io Hạ tầng {t[5]}, gọi từ trên {t[6]}; trùng dòng đáp án {t[7]}/{t[0]}")
