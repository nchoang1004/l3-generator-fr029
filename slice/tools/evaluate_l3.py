"""Run from the repository root. Does not require LLM credentials or source execution."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evaluation_l3.runner import main

if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
