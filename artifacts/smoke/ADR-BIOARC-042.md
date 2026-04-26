# ADR-BIOARC-042: Consent-aware event/API integration between telemedicine and BioArc EHR

## Status
Accepted in the controlled simulation; pending human deployment approval.

## Decision
Use **Patient Identity Gateway + Consent Boundary + Event/API layer**.

## Rationale
Direct shared database access has predicted coupling `+0.42` and privacy-boundary risk `0.88`. The accepted gateway/event design reduces accepted coupling to `+0.08` and latency to `+12 ms`.

## Verification
- [ ] contract tests
- [ ] consent-bypass tests
- [ ] DDI fault-injection tests
- [ ] audit-completeness tests
- [ ] migration rollback drills

## Traceability
Requirements: REQ-BIO-001, REQ-BIO-002, REQ-BIO-003, REQ-BIO-004, REQ-BIO-005, REQ-BIO-006, REQ-BIO-007, REQ-BIO-008
Affected modules: PatientIdentityGateway, ConsentModule, EventLayer, AuditLog, TieredDDIService
