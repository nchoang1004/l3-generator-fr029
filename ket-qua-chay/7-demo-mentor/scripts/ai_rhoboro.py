"""AI run of Khiem's pipeline on rhoboro-demo through run_openai_demo.py (key Open_API from .env, never printed).
Same Pyright fallback as noai_rhoboro.py so both runs differ only by the model."""
import sys
from pathlib import Path

Q = Path("D:/VSF/l3-generator-quote-evidence/experiments/quote-evidence")
sys.path.insert(0, str(Q))
import names  # noqa: E402

names.occurrences = lambda root, scope: {}
import run_openai_demo  # noqa: E402

sys.argv = ["run_openai_demo.py", "D:/VSF/l3-generator-quote-evidence/sample-repos/rhoboro-demo",
            "--out", sys.argv[1], "--oracle", str(Q / "oracle/rhoboro-async-fastapi-sqlalchemy.json")]
run_openai_demo.main()
