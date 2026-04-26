from __future__ import annotations
import csv, json
from dataclasses import asdict
from pathlib import Path
from .data import REQS, RULES, ARCHITECTURE_QUALITY, NEGOTIATION_RESULTS, IMPACT_PREDICTION, ABLATION, CONVERGENCE, MATRIX_LABELS, MATRIX
from .models import NegotiationResult

def write_json(path: Path, obj) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
    return path

def write_csv(path: Path, rows: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        if not rows: return path
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    return path

def write_matrix(path: Path) -> Path:
    rows=[]
    for label, vals in zip(MATRIX_LABELS, MATRIX):
        row={"requirement":label}; row.update({MATRIX_LABELS[i]: vals[i] for i in range(len(vals))}); rows.append(row)
    return write_csv(path, rows)

def static_data(root: Path) -> list[Path]:
    return [
        write_json(root/"data/requirements/bioarc_requirements.json", [asdict(x) for x in REQS]),
        write_json(root/"data/constraints/bioarc_guard_rules.json", [asdict(x) for x in RULES]),
        write_csv(root/"data/simulated/architecture_quality.csv", ARCHITECTURE_QUALITY),
        write_csv(root/"data/simulated/negotiation_results.csv", NEGOTIATION_RESULTS),
        write_csv(root/"data/simulated/impact_prediction.csv", IMPACT_PREDICTION),
        write_csv(root/"data/simulated/ablation_results.csv", ABLATION),
        write_csv(root/"data/simulated/convergence.csv", CONVERGENCE),
        write_matrix(root/"data/simulated/requirement_interaction_matrix.csv"),
    ]

def svg_bar(path: Path, title: str, rows: list[dict], label_key: str, value_key: str) -> Path:
    w,h=820,420; ml,mb,mt=70,95,50; pw=w-110; ph=h-mt-mb; mv=max(float(r[value_key]) for r in rows)
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="white"/><text x="{w/2}" y="28" text-anchor="middle" font-size="18" font-family="Arial">{title}</text>']
    parts.append(f'<line x1="{ml}" y1="{h-mb}" x2="{w-35}" y2="{h-mb}" stroke="#333"/><line x1="{ml}" y1="{mt}" x2="{ml}" y2="{h-mb}" stroke="#333"/>')
    step=pw/len(rows); bw=step*.65
    for i,r in enumerate(rows):
        v=float(r[value_key]); x=ml+i*step+step*.15; bh=v/mv*ph; y=h-mb-bh
        label=str(r[label_key])
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="#4F81BD"/><text x="{x+bw/2:.1f}" y="{y-5:.1f}" text-anchor="middle" font-size="12" font-family="Arial">{v:.2f}</text><text x="{x+bw/2:.1f}" y="{h-mb+20}" text-anchor="end" font-size="11" font-family="Arial" transform="rotate(-35 {x+bw/2:.1f},{h-mb+20})">{label}</text>')
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text("\n".join(parts+["</svg>"]), encoding="utf-8"); return path

def svg_line(path: Path) -> Path:
    w,h=820,420; ml,mb,mt,mr=70,55,50,150; pw=w-ml-mr; ph=h-mt-mb; xs=[r["round"] for r in CONVERGENCE]
    series={"Clinical utility":[r["clinical_utility"] for r in CONVERGENCE],"Technical utility":[r["technical_utility"] for r in CONVERGENCE],"Nash product":[r["nash_product"] for r in CONVERGENCE]}; colors=["#4F81BD","#C0504D","#9BBB59"]
    def xy(x,y): return ml+(x-min(xs))/(max(xs)-min(xs))*pw, mt+(1-y)*ph
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="white"/><text x="{w/2}" y="28" text-anchor="middle" font-size="18" font-family="Arial">Negotiation convergence</text><line x1="{ml}" y1="{h-mb}" x2="{w-mr}" y2="{h-mb}" stroke="#333"/><line x1="{ml}" y1="{mt}" x2="{ml}" y2="{h-mb}" stroke="#333"/>']
    for j,(name,vals) in enumerate(series.items()):
        pts=" ".join(f"{xy(x,y)[0]:.1f},{xy(x,y)[1]:.1f}" for x,y in zip(xs,vals)); parts.append(f'<polyline fill="none" stroke="{colors[j]}" stroke-width="3" points="{pts}"/>')
        parts.append(f'<rect x="{w-mr+20}" y="{mt+j*24}" width="12" height="12" fill="{colors[j]}"/><text x="{w-mr+38}" y="{mt+11+j*24}" font-size="12" font-family="Arial">{name}</text>')
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text("\n".join(parts+["</svg>"]), encoding="utf-8"); return path

def svg_heatmap(path: Path) -> Path:
    cell=76; ml=155; mt=70; w=720; h=600
    def color(v):
        v=max(-1,min(1,v))
        if v>=0: return f"#ff{int(255*(1-v)):02x}{int(255*(1-v)):02x}"
        return f"#{int(255*(1+v)):02x}{int(255*(1+v)):02x}ff"
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="white"/><text x="{w/2}" y="28" text-anchor="middle" font-size="18" font-family="Arial">Requirement interaction matrix</text>']
    for i,l in enumerate(MATRIX_LABELS):
        parts.append(f'<text x="{ml-10}" y="{mt+i*cell+cell/2}" text-anchor="end" font-size="12" font-family="Arial">{l}</text>')
    for r,row in enumerate(MATRIX):
        for c,v in enumerate(row):
            x=ml+c*cell; y=mt+r*cell; parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{color(v)}" stroke="white"/><text x="{x+cell/2}" y="{y+cell/2}" text-anchor="middle" font-size="12" font-family="Arial">{v:.2f}</text>')
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text("\n".join(parts+["</svg>"]), encoding="utf-8"); return path

def bioarc_artifacts(out: Path, res: NegotiationResult) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    tests="\n".join(f"- [ ] {t}" for t in res.accepted.required_tests)
    adr=f"""# ADR-BIOARC-042: Consent-aware event/API integration between telemedicine and BioArc EHR

## Status
Accepted in the controlled simulation; pending human deployment approval.

## Decision
Use **{res.accepted.title}**.

## Rationale
Direct shared database access has predicted coupling `+0.42` and privacy-boundary risk `0.88`. The accepted gateway/event design reduces accepted coupling to `+{res.impact.delta_coupling:.2f}` and latency to `+{res.impact.latency_ms} ms`.

## Verification
{tests}

## Traceability
Requirements: {", ".join(res.accepted.requirement_ids)}
Affected modules: {", ".join(res.impact.affected_modules)}
"""
    trace=[{"requirement_id":rid,"affected_modules":";".join(mods),"accepted_proposal":res.accepted.id,"adr":"ADR-BIOARC-042","tests":";".join(res.accepted.required_tests)} for rid,mods in res.traceability.items()]
    files=[write_json(out/"bioarc_result.json", res.to_dict()), write_csv(out/"bioarc_alternatives.csv", res.alternatives), write_csv(out/"traceability_matrix.csv", trace)]
    (out/"ADR-BIOARC-042.md").write_text(adr, encoding="utf-8"); files.append(out/"ADR-BIOARC-042.md")
    (out/"migration_plan.md").write_text("# BioArc migration plan\n\n1. Introduce PatientIdentityGateway.\n2. Route all sharing through ConsentModule.\n3. Use versioned API and event contracts.\n4. Emit audit events.\n5. Preserve Tier 1 local DDI blocking and Tier 2 async advisories.\n", encoding="utf-8"); files.append(out/"migration_plan.md")
    (out/"test_obligations.md").write_text("# Generated test obligations\n\n"+tests+"\n", encoding="utf-8"); files.append(out/"test_obligations.md")
    return files

def experiment_tables(out: Path) -> list[Path]:
    return [write_csv(out/"architecture_quality.csv", ARCHITECTURE_QUALITY), write_csv(out/"negotiation_results.csv", NEGOTIATION_RESULTS), write_csv(out/"impact_prediction.csv", IMPACT_PREDICTION), write_csv(out/"ablation_results.csv", ABLATION), write_csv(out/"convergence.csv", CONVERGENCE), write_matrix(out/"requirement_interaction_matrix.csv")]

def figures(out: Path) -> list[Path]:
    return [svg_line(out/"convergence.svg"), svg_heatmap(out/"requirement_interaction_matrix.svg"), svg_bar(out/"ablation.svg", "Ablation study", ABLATION, "variant", "overall_success_score")]
