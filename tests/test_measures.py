from __future__ import annotations

from datetime import date

from clinicaliq.care_gaps.identifier import identify_care_gaps
from clinicaliq.measures.catalog import DEFAULT_MEASURES, DiabetesA1CControl, HypertensionBPControl
from clinicaliq.sample_data import sample_patients


def test_diabetes_a1c_control_hand_calculated() -> None:
    result = DiabetesA1CControl().evaluate(sample_patients(), date(2026, 12, 31))

    assert result.denominator_count == 2
    assert result.numerator_count == 1
    assert result.performance_rate == 0.5
    assert result.numerator == ["patient-diabetes-controlled"]


def test_hypertension_bp_control_hand_calculated() -> None:
    result = HypertensionBPControl().evaluate(sample_patients(), date(2026, 12, 31))

    assert result.denominator_count == 1
    assert result.numerator_count == 1
    assert result.performance_rate == 1.0


def test_care_gaps_identify_denominator_not_numerator() -> None:
    gaps = identify_care_gaps(sample_patients(), DEFAULT_MEASURES, date(2026, 12, 31))
    gap_keys = {(gap.patient_id, gap.measure_id) for gap in gaps}

    assert ("patient-diabetes-gap", "DM_A1C_CONTROL") in gap_keys
    assert ("patient-ascvd-gap", "STATIN_THERAPY") in gap_keys
