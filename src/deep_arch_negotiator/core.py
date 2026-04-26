from __future__ import annotations
from math import prod
from .models import Impact, Proposal, GuardResult, Violation, NegotiationResult
from .data import PROPOSALS, REQS, DISAGREEMENT

AGENTS = ["clinical","technical","security_privacy","devops","regulatory","product"]

def clamp(x: float) -> float:
    return round(max(0.0, min(1.0, x)), 4)

class ArchitectureImpactOracle:
    def predict(self, p: Proposal) -> Impact:
        if p.pattern == "direct_db":
            return Impact(0.42,0.22,0.28,0.40,0.65,0.35,40,0.88,["TeleConsultationService","MedicationRepository","ConsentModule","AuditLog","IdentityService"],"Direct database access crosses medication, consent, audit, and identity boundaries.")
        if p.pattern == "sync_api":
            return Impact(0.20,0.10,0.12,0.24,0.30,0.14,120,0.18,["VersionedAPI","ConsentModule","AuditLog","BioArcEHR","TeleConsultationService"],"Synchronous API integration avoids shared tables but creates latency risk.")
        if p.pattern == "gateway_event":
            return Impact(0.08,0.03,0.04,0.10,0.20,0.05,12,0.05,["PatientIdentityGateway","ConsentModule","EventLayer","AuditLog","TieredDDIService"],"Gateway/event design localizes identity, consent, audit, and DDI responsibilities.")
        if p.pattern == "strangler_adapter":
            return Impact(0.12,0.05,0.08,0.15,0.36,0.08,22,0.07,["StranglerFacade","ConsentModule","EventLayer","AuditLog","BioArcEHR"],"Strangler adapter is safe but carries higher migration complexity.")
        return Impact(0.10,0.05,0.06,0.12,0.20,0.05,15,0.05,["UnknownModule"],"Fallback estimate.")

class ArchitectureConsistencyGuard:
    def check(self, p: Proposal, impact: Impact | None = None) -> GuardResult:
        v: list[Violation] = []
        if not p.uses_consent_boundary: v.append(Violation("G-PRIV-01","privacy","Missing Consent Boundary."))
        if p.direct_db_access: v.append(Violation("G-PRIV-02","privacy","Direct medication-table access is prohibited."))
        if not p.audit_events: v.append(Violation("G-AUD-01","audit","Missing audit events for cross-system access."))
        if not p.tier1_local_blocking:
            v.append(Violation("G-SAFE-01","safety","Tier 1 DDI must block lethal interactions."))
            v.append(Violation("G-SAFE-02","safety","Vendor outage must not disable Tier 1 local DDI checks."))
        if not p.uses_identity_gateway: v.append(Violation("G-ARCH-01","architecture","Identity matching must use Patient Identity Gateway."))
        if p.shared_db_access: v.append(Violation("G-ARCH-02","architecture","Shared database access is prohibited without ADR and contract tests."))
        if p.removes_existing_behavior: v.append(Violation("G-BEH-01","behavior","Cannot remove behavior without renegotiation."))
        if impact and impact.privacy_boundary_risk >= 0.80: v.append(Violation("G-PRIV-RISK","privacy","Privacy-boundary risk is too high."))
        return GuardResult(not v, v)

def utilities(p: Proposal, impact: Impact, guard: GuardResult) -> dict[str, float]:
    hp = min(0.8, 0.10 * guard.hard_violation_count)
    arch = impact.architecture_cost()
    lat = min(0.35, impact.latency_ms / 350.0)
    mig = min(0.25, p.migration_points / 20.0)
    return {
        "clinical": clamp(p.clinical_value - 0.30*impact.behavior_risk - 0.08*(not p.tier2_async) - 0.04*hp),
        "technical": clamp(0.94 - 1.75*arch - 0.30*impact.delta_coupling - 0.12*p.migration_points/5.0 - hp),
        "security_privacy": clamp(0.96 - impact.privacy_boundary_risk - hp),
        "devops": clamp(0.92 - lat - mig - 0.05*(not p.uses_event_api) - 0.03*guard.hard_violation_count),
        "regulatory": clamp(0.95 - 0.18*guard.hard_violation_count - 0.30*(not p.audit_events)),
        "product": clamp(0.82 + 0.12*p.clinical_value - 0.12*p.implementation_cost - 0.05*p.migration_points/5.0 - 0.08*guard.hard_violation_count),
    }

def nash_score(u: dict[str, float]) -> float:
    gains = [max(0.0, u[a] - DISAGREEMENT) for a in AGENTS]
    if any(g <= 0 for g in gains): return 0.0
    return round(prod(gains) ** (1/len(gains)), 4)

def traceability(ids: list[str]) -> dict[str, list[str]]:
    d = {r.id: r.affected_modules for r in REQS}
    return {rid: d[rid] for rid in ids if rid in d}

def negotiate(proposals: list[Proposal] | None = None) -> NegotiationResult:
    proposals = proposals or PROPOSALS
    oracle = ArchitectureImpactOracle(); guarder = ArchitectureConsistencyGuard()
    items = []
    for p in proposals:
        imp = oracle.predict(p); grd = guarder.check(p, imp); u = utilities(p, imp, grd); ns = nash_score(u)
        items.append({"proposal":p,"impact":imp,"guard":grd,"utilities":u,"nash_score":ns})
    feasible = [x for x in items if x["guard"].passed]
    best = max(feasible, key=lambda x: (x["nash_score"], -x["impact"].delta_coupling))
    alternatives = []
    for x in items:
        p=x["proposal"]; imp=x["impact"]; grd=x["guard"]
        alternatives.append({"id":p.id,"title":p.title,"pattern":p.pattern,"coupling_delta":imp.delta_coupling,"latency_ms":imp.latency_ms,"privacy_boundary_risk":imp.privacy_boundary_risk,"architecture_cost":imp.architecture_cost(),"guard_passed":grd.passed,"hard_violations":grd.hard_violation_count,"nash_score":x["nash_score"],"utilities":x["utilities"],"reason":imp.explanation})
    accepted = best["proposal"]
    return NegotiationResult(accepted, best["impact"], best["guard"], best["utilities"], best["nash_score"], 0.85 if accepted.id=="gateway_event" else 0.65, alternatives, traceability(accepted.requirement_ids))
