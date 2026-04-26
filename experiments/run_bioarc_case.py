from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT/"src"))
from deep_arch_negotiator.experiments import run_bioarc
p=argparse.ArgumentParser(); p.add_argument("--out", default=str(ROOT/"artifacts")); a=p.parse_args()
print(json.dumps(run_bioarc(a.out), indent=2, ensure_ascii=False))
