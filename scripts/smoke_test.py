from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT/"src"))
from deep_arch_negotiator.experiments import run_all
from deep_arch_negotiator.core import negotiate
OUT=ROOT/"artifacts"/"smoke"
OUT.mkdir(parents=True, exist_ok=True)
summary=run_all(OUT)
res=negotiate()
assert res.accepted.id == "gateway_event"
assert res.impact.delta_coupling == 0.08
assert res.impact.latency_ms == 12
assert res.guard.hard_violation_count == 0
assert res.adoption_rate == 0.85
direct=next(x for x in res.alternatives if x["id"]=="direct_db")
assert direct["coupling_delta"] == 0.42
assert direct["guard_passed"] is False
required=["bioarc_result.json","ADR-BIOARC-042.md","traceability_matrix.csv","migration_plan.md","test_obligations.md","architecture_quality.csv","negotiation_results.csv","impact_prediction.csv","ablation_results.csv","convergence.svg","requirement_interaction_matrix.svg","ablation.svg"]
for name in required:
    assert (OUT/name).exists(), f"missing {name}"
report={"status":"passed","accepted_proposal":res.accepted.id,"coupling_delta":res.impact.delta_coupling,"latency_ms":res.impact.latency_ms,"adoption_rate":res.adoption_rate,"artifact_count":len(required)}
(OUT/"SMOKE_TEST_REPORT.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2), flush=True)
