from __future__ import annotations
from dataclasses import dataclass, asdict, field

@dataclass(frozen=True)
class Requirement:
    id: str
    text: str
    priority: str
    primary_risk: str
    clinical_value: float
    affected_modules: list[str]

@dataclass(frozen=True)
class GuardRule:
    id: str
    text: str
    category: str

@dataclass(frozen=True)
class Proposal:
    id: str
    title: str
    pattern: str
    requirement_ids: list[str]
    clinical_value: float
    implementation_cost: float
    uses_identity_gateway: bool = False
    uses_consent_boundary: bool = False
    uses_event_api: bool = False
    uses_versioned_api: bool = False
    audit_events: bool = False
    direct_db_access: bool = False
    shared_db_access: bool = False
    synchronous_all_calls: bool = False
    tier1_local_blocking: bool = False
    tier2_async: bool = False
    removes_existing_behavior: bool = False
    migration_points: int = 0
    required_tests: list[str] = field(default_factory=list)

@dataclass(frozen=True)
class Impact:
    delta_coupling: float
    delta_cohesion_loss: float
    delta_modularity_loss: float
    delta_change_impact: float
    migration_risk: float
    behavior_risk: float
    latency_ms: int
    privacy_boundary_risk: float
    affected_modules: list[str]
    explanation: str
    def architecture_cost(self) -> float:
        a = {"c":0.35,"h":0.20,"m":0.15,"ch":0.10,"mi":0.10,"b":0.10}
        return round(a["c"]*self.delta_coupling + a["h"]*self.delta_cohesion_loss + a["m"]*self.delta_modularity_loss + a["ch"]*self.delta_change_impact + a["mi"]*self.migration_risk + a["b"]*self.behavior_risk, 4)

@dataclass(frozen=True)
class Violation:
    rule_id: str
    category: str
    message: str

@dataclass(frozen=True)
class GuardResult:
    passed: bool
    violations: list[Violation]
    @property
    def hard_violation_count(self) -> int:
        return len(self.violations)

@dataclass(frozen=True)
class NegotiationResult:
    accepted: Proposal
    impact: Impact
    guard: GuardResult
    utilities: dict[str, float]
    nash_score: float
    adoption_rate: float
    alternatives: list[dict]
    traceability: dict[str, list[str]]
    def to_dict(self) -> dict:
        return {
            "accepted": asdict(self.accepted),
            "impact": asdict(self.impact) | {"architecture_cost": self.impact.architecture_cost()},
            "guard": {"passed": self.guard.passed, "hard_violation_count": self.guard.hard_violation_count, "violations": [asdict(v) for v in self.guard.violations]},
            "utilities": self.utilities,
            "nash_score": self.nash_score,
            "adoption_rate": self.adoption_rate,
            "alternatives": self.alternatives,
            "traceability": self.traceability,
        }
