# ClinicalIQ

ClinicalIQ is a FHIR-native clinical outcomes analytics platform for synthetic patient data. It validates
FHIR-style bundles, normalizes clinical resources into analytics marts, computes HEDIS-style quality measures,
identifies care gaps, and exposes the results through API/dashboard entrypoints.

This project is distinct from `healthcare-denial-risk-ai`: that project is revenue-cycle and billing-side.
ClinicalIQ is clinical-side population health analytics.

## Current MVP

- FHIR Bundle validation and resource parsing
- Patient-level normalization for Patient, Condition, Observation, Procedure, Immunization, and MedicationRequest
- Six HEDIS-style educational quality measures
- Hand-calculated pytest coverage for measure logic
- Care gap identification and risk prioritization
- Rule-based clinical NLP fallback for problems and SDOH flags
- FastAPI and Streamlit entrypoints
- HIPAA-design documentation for synthetic-data portfolio use

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
docker compose up -d
```

Optional app dependencies:

```powershell
python -m pip install -e ".[app]"
uvicorn clinicaliq.apps.api.main:app --reload
streamlit run src/clinicaliq/apps/dashboard/streamlit_app.py
```

## Synthea Plan

Generate synthetic Massachusetts patients with Synthea:

```bash
./run_synthea -p 10000 Massachusetts
```

Place generated FHIR bundles under `data/synthea_output/`. This folder is intentionally gitignored.

## Test Plan

- Unit tests validate FHIR parsing and normalization.
- Hand-calculated tests validate quality measure denominator/numerator logic.
- Care gap tests verify denominator-not-numerator patient worklists.
- NLP/redaction tests verify SDOH extraction and PHI-safe logging behavior.

## Milestone Resume Bullet

Built ClinicalIQ, a FHIR-native clinical analytics MVP that validates synthetic FHIR bundles, normalizes patient resources, computes six HEDIS-style quality measures with hand-tested numerator/denominator logic, and generates prioritized care gap worklists for population health workflows.

## LinkedIn Snippet

Started ClinicalIQ, a clinical-side population health analytics platform using FHIR-style data, quality measure logic, care gap identification, and HIPAA-minded engineering patterns. The goal is to demonstrate healthcare interoperability, clinical analytics, and care manager workflow design for Boston-area clinical analytics roles.

