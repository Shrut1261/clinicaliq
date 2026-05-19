# HIPAA Design Notes

ClinicalIQ uses synthetic data only, but it is written with production clinical controls in mind.

- No PHI in logs: application logging runs through redaction helpers.
- Audit events: ingestion and access patterns should emit structured audit events.
- Encryption in transit: production APIs should require TLS everywhere.
- Encryption at rest: production Postgres volumes and object storage should use managed encryption.
- Access control: production dashboards should use SSO, least privilege roles, and patient-level access checks.
- Vendor controls: any production deployment handling PHI needs BAAs with infrastructure providers.
- Data minimization: dashboard and API responses should return only fields required for the workflow.

