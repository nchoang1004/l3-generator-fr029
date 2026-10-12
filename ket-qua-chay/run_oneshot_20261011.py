"""FR-029 one-shot mode on Teamhide. Model, prices, cap: env MODEL, PRICES, CAP_USD, MAX_OUT, EFFORT.

Usage: python ket-qua-chay/run_oneshot_20261011.py <out_dir> [--dry]
--dry: build the first request, print its size and an upper cost bound, send nothing.
The key comes from OPENAI_API_KEY (set by the with_openai.py wrapper); it is never printed.
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path("slice").resolve()))
from l3slice.docagent import Budget, OpenAICompatProvider, ProviderError  # noqa: E402
from l3slice.docpipeline import run_documents  # noqa: E402

SOURCE = Path("D:/VSF/l3-generator-quote-evidence/sample-repos/teamhide_fastapi-boilerplate-df4e6d4")
MEMBERSHIP = Path("ket-qua-chay/fr029-20261002/teamhide-existing.membership.json")
MODEL = os.environ.get("MODEL", "gpt-4.1-mini-2025-04-14")
# USD per 1M tokens: input, cached input, output (default gpt-4.1-mini)
PRICES = tuple(float(x) for x in os.environ.get("PRICES", "0.4,0.1,1.6").split(","))
CAP_USD, MAX_OUT = float(os.environ.get("CAP_USD", "0.20")), int(os.environ.get("MAX_OUT", "16000"))
EFFORT = os.environ.get("EFFORT") or None  # reasoning effort for reasoning models

root = Path(sys.argv[1])
dry = "--dry" in sys.argv
root.mkdir(parents=True, exist_ok=True)
provider = OpenAICompatProvider("https://api.openai.com/v1", MODEL, "OPENAI_API_KEY", max_output_tokens=MAX_OUT,
                                reasoning_effort=EFFORT, prices=PRICES, timeout=600)
provider.WAITS, provider.NET_RETRIES = 0, 0
ledger, original = [], urllib.request.urlopen


def guarded(req, *a, **kw):
    """Refuse a request whose worst case (every byte a full-price token, full answer) would pass the cap."""
    if not isinstance(req, urllib.request.Request) or req.full_url != "https://api.openai.com/v1/chat/completions":
        raise ProviderError("UNEXPECTED_ENDPOINT", False)
    payload = json.loads(req.data)
    # measured 3.7 bytes per token on this source; 3 keeps the bound above the real input
    upper = (len(req.data) / 3 * PRICES[0] + payload["max_completion_tokens"] * PRICES[2]) / 1e6
    entry = {"request": len(ledger) + 1, "bytes": len(req.data), "upper_usd": round(upper, 6),
             "spent_before_usd": round(provider.cost_usd, 6)}
    ledger.append(entry)
    (root / "budget.json").write_text(json.dumps(ledger, indent=1), encoding="utf-8")
    print("request", entry, flush=True)
    if dry:
        raise ProviderError("DRY_RUN", False)
    if provider.cost_usd + upper > CAP_USD:
        raise ProviderError("LOCAL_BUDGET_RESERVATION_STOP", False)
    return original(req, *a, **kw)


urllib.request.urlopen = guarded
try:
    data = run_documents(SOURCE, root / "output", MEMBERSHIP, "teamhide", provider, mode="oneshot",
                         checkpoint=root / "checkpoint.json",
                         budget=Budget(max_seconds=900, retries=0, max_cost_usd=CAP_USD, max_repair_rounds=2),
                         run_id="run_oneshot_teamhide_20261011")
    print("STATUS", data["agent"]["status"], data["agent"]["reason"], flush=True)
except Exception as e:  # noqa: BLE001 - the type is enough; messages may echo provider text
    print("ERROR_TYPE", type(e).__name__, flush=True)
finally:
    (root / "cost.json").write_text(json.dumps({"model": provider.model, "effort": EFFORT, "prices": PRICES, "usage_based_cost_usd": provider.cost_usd,
                                                "requests": len(ledger), "cap_usd": CAP_USD}, indent=1), encoding="utf-8")
    print("COST", round(provider.cost_usd, 6), flush=True)
