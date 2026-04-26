from __future__ import annotations
import argparse, json
from pathlib import Path
from .experiments import run_all, run_bioarc, run_ablation, run_impact

def main(argv=None) -> int:
    p=argparse.ArgumentParser(prog="deep-arch-negotiator"); sub=p.add_subparsers(dest="cmd", required=True)
    for name in ["run-all","bioarc","ablation","impact"]:
        sp=sub.add_parser(name); sp.add_argument("--out", default="artifacts")
    a=p.parse_args(argv)
    fn={"run-all":run_all,"bioarc":run_bioarc,"ablation":run_ablation,"impact":run_impact}[a.cmd]
    print(json.dumps(fn(Path(a.out)), indent=2, ensure_ascii=False)); return 0
if __name__ == "__main__": raise SystemExit(main())
