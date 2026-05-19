from __future__ import annotations

from datetime import date

from clinicaliq.ingest.normalize import ClinicalEvent, PatientRecord


def sample_patients() -> list[PatientRecord]:
    return [
        PatientRecord(
            patient_id="patient-diabetes-controlled",
            birth_date=date(1968, 5, 1),
            sex="female",
            conditions=[ClinicalEvent("44054006", "SNOMED", "Diabetes", date(2020, 1, 1))],
            observations=[
                ClinicalEvent("4548-4", "LOINC", "Hemoglobin A1c", date(2026, 6, 1), 7.2, "%")
            ],
            procedures=[ClinicalEvent("24606-6", "LOINC", "Mammogram", date(2025, 7, 1))],
        ),
        PatientRecord(
            patient_id="patient-diabetes-gap",
            birth_date=date(1975, 7, 1),
            sex="male",
            conditions=[ClinicalEvent("44054006", "SNOMED", "Diabetes", date(2022, 1, 1))],
            observations=[
                ClinicalEvent("4548-4", "LOINC", "Hemoglobin A1c", date(2026, 6, 1), 10.1, "%")
            ],
        ),
        PatientRecord(
            patient_id="patient-htn-controlled",
            birth_date=date(1960, 3, 12),
            sex="male",
            conditions=[ClinicalEvent("38341003", "SNOMED", "Hypertension", date(2018, 1, 1))],
            observations=[
                ClinicalEvent("8480-6", "LOINC", "Systolic BP", date(2026, 9, 1), 128, "mmHg"),
                ClinicalEvent("8462-4", "LOINC", "Diastolic BP", date(2026, 9, 1), 78, "mmHg"),
            ],
        ),
        PatientRecord(
            patient_id="patient-ascvd-gap",
            birth_date=date(1959, 8, 1),
            sex="female",
            conditions=[ClinicalEvent("53741008", "SNOMED", "ASCVD", date(2020, 1, 1))],
        ),
    ]
