# DeepArchNegotiator

Reference GitHub repository for the paper **Stakeholder-Aware Software Architecture Refactoring via Graph Neural Modularization and Multi-Agent Requirements Negotiation**.

This repo is an executable, deterministic replication package for the controlled BioArc experiments in the manuscript. It keeps the same concepts as the paper: a heterogeneous requirement-architecture-code graph, an architecture-impact oracle, multi-agent utilities, guarded Nash-style negotiation, Architecture Consistency Guard rules, ADR/test/migration artifacts, ablations, and impact-prediction metrics.

> Scope: this is a lightweight reference implementation. It does not train a real GNN or call LLM APIs. The oracle is a transparent surrogate encoding the controlled-simulation values reported in the paper so the experimental protocol can be tested end-to-end.

## Main paper points captured in code

- Architecture refactoring is modeled as a stakeholder negotiation problem, not just clustering.
- Technical utility includes predicted architecture impact: coupling, cohesion loss, modularity loss, change impact, migration risk, and behavior risk.
- Candidate BioArc designs are evaluated under hard privacy, audit, safety, and architecture guard rules.
- Direct shared database access is rejected because it creates high coupling and privacy-boundary risk.
- The negotiated gateway/event design is selected and emits ADRs, traceability, migration plan, and test obligations.

## Expected controlled-simulation values

| Quantity | Expected value |
|---|---:|
| Direct DB predicted coupling increase | `+0.42` |
| Gateway/event predicted coupling increase | `+0.08` |
| All-synchronous API latency-risk path | `+120 ms` |
| Gateway/event latency | `+12 ms` |
| DeepArchNegotiator adoption | `85%` |
| Final hard violations | `0` |
| Full-system ablation score | `0.88` |

## Layout

```text
src/deep_arch_negotiator/   Python package
experiments/                executable experiment wrappers
scripts/smoke_test.py       smoke test used before release
tests/                      unit tests
data/                       JSON/CSV simulation fixtures
artifacts/                  generated outputs
paper/                      manuscript source PDF/TEX
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python experiments/run_all.py --out artifacts
python scripts/smoke_test.py
python -m unittest discover -s tests -v
```

After running, inspect:

- `artifacts/bioarc_result.json`
- `artifacts/ADR-BIOARC-042.md`
- `artifacts/traceability_matrix.csv`
- `artifacts/migration_plan.md`
- `artifacts/test_obligations.md`
- `artifacts/architecture_quality.csv`
- `artifacts/negotiation_results.csv`
- `artifacts/impact_prediction.csv`
- `artifacts/ablation_results.csv`
- `artifacts/convergence.svg`
- `artifacts/requirement_interaction_matrix.svg`
- `artifacts/ablation.svg`

## CLI

```bash
deep-arch-negotiator run-all --out artifacts
deep-arch-negotiator bioarc --out artifacts
deep-arch-negotiator ablation --out artifacts
deep-arch-negotiator impact --out artifacts
```

## Ethical note

This package is decision support for architecture research. Healthcare architecture changes still require human review, privacy governance, domain validation, and safety approval before deployment.
