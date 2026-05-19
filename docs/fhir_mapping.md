# FHIR to Mart Mapping

| FHIR Resource | Mart Table | Purpose |
|---|---|---|
| Patient | mart.dim_patient | Demographics, age, sex, geography |
| Encounter | mart.fact_encounter | Care utilization and risk stratification |
| Observation | mart.fact_observation | A1c, blood pressure, labs, vitals |
| Condition | mart.fact_condition | Diabetes, hypertension, ASCVD, chronic disease cohorts |
| Procedure | mart.fact_procedure | Mammogram, colorectal screening, preventive care |
| MedicationRequest | mart.fact_medication_request | Statin therapy and medication adherence signals |
| Immunization | mart.fact_immunization | Childhood immunization measure logic |

