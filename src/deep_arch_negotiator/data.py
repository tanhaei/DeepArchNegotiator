from __future__ import annotations
from .models import Requirement, GuardRule, Proposal

DISAGREEMENT = 0.20

REQS = [
    Requirement("REQ-BIO-001", "Identify patients through a shared patient identity gateway before reading or writing clinical records.", "Must-have", "Identity coupling", 0.94, ["IdentityService", "TeleConsultationService", "PatientIdentityGateway"]),
    Requirement("REQ-BIO-002", "Enforce explicit consent before encounter summaries are transferred to BioArc.", "Must-have", "Privacy boundary", 0.96, ["ConsentModule", "TeleConsultationService", "AuditLog"]),
    Requirement("REQ-BIO-003", "Perform Tier 1 DDI checks synchronously for life-threatening pairs.", "Must-have", "Safety-latency", 0.98, ["PrescriptionWorkflow", "TieredDDIService", "MedicationRepository"]),
    Requirement("REQ-BIO-004", "Evaluate Tier 2 medication advisories asynchronously and route them to notification or pharmacist queues.", "Performance", "Workflow disruption", 0.82, ["TieredDDIService", "NotificationQueue", "PharmacistQueue"]),
    Requirement("REQ-BIO-005", "Generate audit events for all cross-system access with user, patient, purpose, timestamp, and consent reference.", "Must-have", "Audit volume", 0.91, ["AuditLog", "EventLayer", "ConsentModule"]),
    Requirement("REQ-BIO-006", "Appointment and billing data shall not directly access clinical medication tables.", "Constraint", "Database coupling", 0.88, ["AppointmentService", "BillingService", "MedicationRepository"]),
    Requirement("REQ-BIO-007", "Write teleconsultation notes through a versioned API contract rather than shared database writes.", "Must-have", "API evolution", 0.89, ["TeleConsultationService", "VersionedAPI", "BioArcEHR"]),
    Requirement("REQ-BIO-008", "Offline or vendor-failure DDI behavior shall preserve Tier 1 blocking while allowing Tier 2 soft-fail.", "Must-have", "Availability/safety", 0.93, ["TieredDDIService", "LocalSafetyCache", "VendorDDIAdapter"]),
]

RULES = [
    GuardRule("G-PRIV-01", "No module outside the Consent Boundary may transfer clinical encounter data without an active consent reference.", "privacy"),
    GuardRule("G-PRIV-02", "Telemedicine services may not directly read or write medication tables; all access must occur through a versioned API or approved event contract.", "privacy"),
    GuardRule("G-AUD-01", "Every cross-system clinical data access must emit an audit event containing user, patient, purpose, timestamp, and consent reference.", "audit"),
    GuardRule("G-SAFE-01", "Tier 1 life-threatening DDI checks must block prescription signing if a known lethal interaction is detected.", "safety"),
    GuardRule("G-SAFE-02", "Vendor/API outage may not disable Tier 1 local DDI checks.", "safety"),
    GuardRule("G-ARCH-01", "Patient identity matching must be performed only by the Patient Identity Gateway.", "architecture"),
    GuardRule("G-ARCH-02", "Shared database access is prohibited unless explicitly approved by an ADR and covered by contract tests.", "architecture"),
    GuardRule("G-BEH-01", "Refactoring may not remove existing prescription, consent, or audit behavior unless renegotiated.", "behavior"),
]

ALL_IDS = [r.id for r in REQS]
PROPOSALS = [
    Proposal("direct_db", "Direct shared database access", "direct_db", ALL_IDS, 0.96, 0.24, direct_db_access=True, shared_db_access=True, migration_points=1, required_tests=["differential integration tests"]),
    Proposal("sync_api", "All-synchronous versioned API integration", "sync_api", ALL_IDS, 0.92, 0.36, uses_identity_gateway=True, uses_consent_boundary=True, uses_versioned_api=True, audit_events=True, synchronous_all_calls=True, tier1_local_blocking=True, migration_points=3, required_tests=["API contract tests", "latency budget tests", "audit completeness tests"]),
    Proposal("gateway_event", "Patient Identity Gateway + Consent Boundary + Event/API layer", "gateway_event", ALL_IDS, 0.94, 0.42, uses_identity_gateway=True, uses_consent_boundary=True, uses_event_api=True, uses_versioned_api=True, audit_events=True, tier1_local_blocking=True, tier2_async=True, migration_points=2, required_tests=["contract tests", "consent-bypass tests", "DDI fault-injection tests", "audit-completeness tests", "migration rollback drills"]),
    Proposal("strangler_adapter", "Strangler migration with interim adapter", "strangler_adapter", ALL_IDS, 0.88, 0.48, uses_identity_gateway=True, uses_consent_boundary=True, uses_event_api=True, uses_versioned_api=True, audit_events=True, tier1_local_blocking=True, tier2_async=True, migration_points=5, required_tests=["facade contract tests", "rollback drills", "audit-completeness tests"]),
]

ARCHITECTURE_QUALITY = [
    {"system":"ACDC","mojofm":65.4,"coupling":0.45,"cohesion":0.30,"semantic_coherence":0.40,"smell_reduction":"12%"},
    {"system":"WCA","mojofm":68.2,"coupling":0.42,"cohesion":0.35,"semantic_coherence":0.42,"smell_reduction":"15%"},
    {"system":"Bunch","mojofm":72.5,"coupling":0.38,"cohesion":0.45,"semantic_coherence":0.45,"smell_reduction":"20%"},
    {"system":"NSGA-II","mojofm":75.1,"coupling":0.35,"cohesion":0.48,"semantic_coherence":0.48,"smell_reduction":"25%"},
    {"system":"DeepModule","mojofm":82.3,"coupling":0.28,"cohesion":0.55,"semantic_coherence":0.65,"smell_reduction":"38%"},
    {"system":"DeepArchNegotiator","mojofm":81.5,"coupling":0.25,"cohesion":0.52,"semantic_coherence":0.68,"smell_reduction":"45%"},
]
NEGOTIATION_RESULTS = [
    {"variant":"MedNegotiator-only","agreement":"85%","rounds":6.2,"nash":0.42,"final_hard_violations":3,"adoption":"75%"},
    {"variant":"LLM-only","agreement":"65%","rounds":4.5,"nash":0.25,"final_hard_violations":12,"adoption":"45%"},
    {"variant":"No GNN oracle","agreement":"78%","rounds":5.8,"nash":0.35,"final_hard_violations":5,"adoption":"68%"},
    {"variant":"No guard","agreement":"92%","rounds":4.1,"nash":0.48,"final_hard_violations":18,"adoption":"50%"},
    {"variant":"No counterproposal","agreement":"55%","rounds":8.5,"nash":0.28,"final_hard_violations":0,"adoption":"60%"},
    {"variant":"DeepArchNegotiator","agreement":"88%","rounds":7.1,"nash":0.45,"final_hard_violations":0,"adoption":"85%"},
]
IMPACT_PREDICTION = [
    {"prediction_target":"delta_coupling","mae":0.05,"rmse":0.08,"spearman_rho":0.82,"affected_module_f1":0.88},
    {"prediction_target":"delta_cohesion","mae":0.06,"rmse":0.09,"spearman_rho":0.79,"affected_module_f1":0.85},
    {"prediction_target":"delta_modularity","mae":0.04,"rmse":0.07,"spearman_rho":0.85,"affected_module_f1":0.90},
    {"prediction_target":"change_impact","mae":0.12,"rmse":0.15,"spearman_rho":0.75,"affected_module_f1":0.82},
    {"prediction_target":"migration_risk","mae":0.15,"rmse":0.18,"spearman_rho":0.71,"affected_module_f1":0.78},
    {"prediction_target":"behavior_risk","mae":0.10,"rmse":0.14,"spearman_rho":0.76,"affected_module_f1":0.80},
]
ABLATION = [{"variant":"Full System","overall_success_score":0.88},{"variant":"No GNN","overall_success_score":0.65},{"variant":"No Nash","overall_success_score":0.72},{"variant":"No Guard","overall_success_score":0.58},{"variant":"No Trace","overall_success_score":0.75},{"variant":"LLM-only","overall_success_score":0.55}]
CONVERGENCE = [{"round":1,"clinical_utility":0.98,"technical_utility":0.25,"nash_product":0.06},{"round":2,"clinical_utility":0.96,"technical_utility":0.31,"nash_product":0.10},{"round":3,"clinical_utility":0.91,"technical_utility":0.44,"nash_product":0.18},{"round":4,"clinical_utility":0.88,"technical_utility":0.56,"nash_product":0.26},{"round":5,"clinical_utility":0.86,"technical_utility":0.65,"nash_product":0.32},{"round":6,"clinical_utility":0.84,"technical_utility":0.69,"nash_product":0.35},{"round":7,"clinical_utility":0.83,"technical_utility":0.71,"nash_product":0.37},{"round":8,"clinical_utility":0.82,"technical_utility":0.73,"nash_product":0.38},{"round":9,"clinical_utility":0.82,"technical_utility":0.73,"nash_product":0.38}]
MATRIX_LABELS = ["REQ-Identity","REQ-Consent","REQ-DDI","REQ-Telemed","REQ-Billing"]
MATRIX = [[1.00,0.85,0.30,0.75,0.40],[0.85,1.00,0.25,0.60,0.10],[0.30,0.25,1.00,0.50,-0.15],[0.75,0.60,0.50,1.00,0.45],[0.40,0.10,-0.15,0.45,1.00]]
