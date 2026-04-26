# BioArc migration plan

1. Introduce PatientIdentityGateway.
2. Route all sharing through ConsentModule.
3. Use versioned API and event contracts.
4. Emit audit events.
5. Preserve Tier 1 local DDI blocking and Tier 2 async advisories.
