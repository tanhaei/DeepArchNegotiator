from __future__ import annotations
from pathlib import Path
from .artifacts import bioarc_artifacts, experiment_tables, figures, static_data
from .core import negotiate
from .data import ABLATION, IMPACT_PREDICTION

def run_bioarc(out_dir: str | Path = "artifacts") -> dict:
    out=Path(out_dir); res=negotiate(); paths=bioarc_artifacts(out,res)
    return {"accepted_proposal":res.accepted.id,"accepted_title":res.accepted.title,"coupling_delta":res.impact.delta_coupling,"latency_ms":res.impact.latency_ms,"final_hard_violations":res.guard.hard_violation_count,"adoption_rate":res.adoption_rate,"nash_score":res.nash_score,"artifacts":[str(p) for p in paths]}

def run_ablation(out_dir: str | Path = "artifacts") -> dict:
    out=Path(out_dir); experiment_tables(out); figs=figures(out); full=next(x for x in ABLATION if x["variant"]=="Full System")
    return {"full_system_score":full["overall_success_score"],"figures":[str(p) for p in figs if "ablation" in p.name]}

def run_impact(out_dir: str | Path = "artifacts") -> dict:
    out=Path(out_dir); experiment_tables(out); figs=figures(out); avg=round(sum(x["mae"] for x in IMPACT_PREDICTION)/len(IMPACT_PREDICTION),4)
    return {"average_mae":avg,"targets":[x["prediction_target"] for x in IMPACT_PREDICTION],"figures":[str(p) for p in figs if "interaction" in p.name]}

def run_all(out_dir: str | Path = "artifacts") -> dict:
    out=Path(out_dir); static=static_data(Path.cwd()); bio=run_bioarc(out); tables=experiment_tables(out); figs=figures(out)
    return {"bioarc":bio,"static_data_files":[str(p) for p in static],"tables":[str(p) for p in tables],"figures":[str(p) for p in figs]}
