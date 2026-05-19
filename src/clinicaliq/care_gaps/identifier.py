from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from clinicaliq.ingest.normalize import PatientRecord
from clinicaliq.measures.engine import QualityMeasure


@dataclass(frozen=True)
class CareGap:
    patient_id: str
    measure_id: str
    risk_tier: str
    reason: str


def identify_care_gaps(
    patients: list[PatientRecord], measures: list[QualityMeasure], as_of: date
) -> list[CareGap]:
    gaps: list[CareGap] = []
    condition_counts = {p.patient_id: len(p.conditions) for p in patients}
    for measure in measures:
        result = measure.evaluate(patients, as_of)
        numerator = set(result.numerator)
        for patient_id in result.denominator:
            if patient_id in numerator:
                continue
            condition_count = condition_counts.get(patient_id, 0)
            risk_tier = (
                "high" if condition_count >= 3 else "medium" if condition_count >= 1 else "low"
            )
            gaps.append(
                CareGap(
                    patient_id=patient_id,
                    measure_id=result.measure_id,
                    risk_tier=risk_tier,
                    reason=(
                        f"Patient is eligible for {result.measure_id} "
                        "but has no qualifying numerator event."
                    ),
                )
            )
    return sorted(gaps, key=lambda gap: {"high": 0, "medium": 1, "low": 2}[gap.risk_tier])
