from __future__ import annotations

from datetime import date

from clinicaliq.ingest.normalize import PatientRecord
from clinicaliq.measures.engine import MeasureResult, QualityMeasure, age_on, within_years
from clinicaliq.measures.value_sets import (
    A1C_LOINC_CODES,
    ASCVD_CODES,
    CHILDHOOD_IMMUNIZATION_CODES,
    COLORECTAL_SCREENING_CODES,
    DIABETES_CODES,
    DIASTOLIC_BP_LOINC_CODES,
    HYPERTENSION_CODES,
    MAMMOGRAM_CODES,
    STATIN_RXNORM_CODES,
    SYSTOLIC_BP_LOINC_CODES,
)


def _has_condition(patient: PatientRecord, codes: set[str]) -> bool:
    return any(condition.code in codes for condition in patient.conditions)


class DiabetesA1CControl:
    measure_id = "DM_A1C_CONTROL"

    def evaluate(self, patients: list[PatientRecord], as_of: date) -> MeasureResult:
        denominator = [p.patient_id for p in patients if _has_condition(p, DIABETES_CODES)]
        numerator = [
            p.patient_id
            for p in patients
            if p.patient_id in denominator
            and any(
                obs.code in A1C_LOINC_CODES
                and obs.value is not None
                and obs.value < 9
                and within_years(obs.date, as_of, 1)
                for obs in p.observations
            )
        ]
        return MeasureResult(self.measure_id, denominator, numerator, [])


class HypertensionBPControl:
    measure_id = "HTN_BP_CONTROL"

    def evaluate(self, patients: list[PatientRecord], as_of: date) -> MeasureResult:
        denominator = [p.patient_id for p in patients if _has_condition(p, HYPERTENSION_CODES)]
        numerator: list[str] = []
        for patient in patients:
            if patient.patient_id not in denominator:
                continue
            systolic = [
                obs
                for obs in patient.observations
                if obs.code in SYSTOLIC_BP_LOINC_CODES and obs.value
            ]
            diastolic = [
                obs
                for obs in patient.observations
                if obs.code in DIASTOLIC_BP_LOINC_CODES and obs.value
            ]
            if any(
                s.value is not None
                and s.value < 140
                and within_years(s.date, as_of, 1)
                and any(
                    d.value is not None
                    and d.value < 90
                    and d.date == s.date
                    and within_years(d.date, as_of, 1)
                    for d in diastolic
                )
                for s in systolic
            ):
                numerator.append(patient.patient_id)
        return MeasureResult(self.measure_id, denominator, numerator, [])


class BreastCancerScreening:
    measure_id = "BCS_SCREENING"

    def evaluate(self, patients: list[PatientRecord], as_of: date) -> MeasureResult:
        denominator = [
            p.patient_id
            for p in patients
            if p.sex == "female"
            and (age := age_on(p.birth_date, as_of)) is not None
            and 50 <= age <= 74
        ]
        numerator = [
            p.patient_id
            for p in patients
            if p.patient_id in denominator
            and any(
                proc.code in MAMMOGRAM_CODES and within_years(proc.date, as_of, 2)
                for proc in p.procedures
            )
        ]
        return MeasureResult(self.measure_id, denominator, numerator, [])


class ColorectalCancerScreening:
    measure_id = "COL_SCREENING"

    def evaluate(self, patients: list[PatientRecord], as_of: date) -> MeasureResult:
        denominator = [
            p.patient_id
            for p in patients
            if (age := age_on(p.birth_date, as_of)) is not None and 50 <= age <= 75
        ]
        numerator = [
            p.patient_id
            for p in patients
            if p.patient_id in denominator
            and any(
                proc.code in COLORECTAL_SCREENING_CODES and within_years(proc.date, as_of, 10)
                for proc in p.procedures
            )
        ]
        return MeasureResult(self.measure_id, denominator, numerator, [])


class ChildhoodImmunizationStatus:
    measure_id = "CIS_COMBO"

    def evaluate(self, patients: list[PatientRecord], as_of: date) -> MeasureResult:
        denominator = [
            p.patient_id
            for p in patients
            if (age := age_on(p.birth_date, as_of)) is not None and age <= 2
        ]
        numerator = [
            p.patient_id
            for p in patients
            if p.patient_id in denominator
            and CHILDHOOD_IMMUNIZATION_CODES.issubset({imm.code for imm in p.immunizations})
        ]
        return MeasureResult(self.measure_id, denominator, numerator, [])


class StatinTherapy:
    measure_id = "STATIN_THERAPY"

    def evaluate(self, patients: list[PatientRecord], as_of: date) -> MeasureResult:
        denominator = [p.patient_id for p in patients if _has_condition(p, ASCVD_CODES)]
        numerator = [
            p.patient_id
            for p in patients
            if p.patient_id in denominator
            and any(
                med.code in STATIN_RXNORM_CODES and within_years(med.date, as_of, 1)
                for med in p.medications
            )
        ]
        return MeasureResult(self.measure_id, denominator, numerator, [])


DEFAULT_MEASURES: list[QualityMeasure] = [
    DiabetesA1CControl(),
    HypertensionBPControl(),
    BreastCancerScreening(),
    ColorectalCancerScreening(),
    ChildhoodImmunizationStatus(),
    StatinTherapy(),
]
