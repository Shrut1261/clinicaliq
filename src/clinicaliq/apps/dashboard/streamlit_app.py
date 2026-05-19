from __future__ import annotations

from datetime import date
from typing import Any

try:
    import streamlit as streamlit_module  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    streamlit_module = None

from clinicaliq.care_gaps.identifier import identify_care_gaps
from clinicaliq.measures.catalog import DEFAULT_MEASURES
from clinicaliq.sample_data import sample_patients

st: Any = streamlit_module

if st is not None:
    st.set_page_config(page_title="ClinicalIQ", layout="wide")
    st.title("ClinicalIQ")
    st.caption("FHIR-native population health quality measures and care gap analytics")

    patients = sample_patients()
    results = [measure.evaluate(patients, date(2026, 12, 31)) for measure in DEFAULT_MEASURES]
    gaps = identify_care_gaps(patients, DEFAULT_MEASURES, date(2026, 12, 31))

    col1, col2, col3 = st.columns(3)
    col1.metric("Patients", len(patients))
    col2.metric("Quality Measures", len(results))
    col3.metric("Open Care Gaps", len(gaps))

    st.subheader("Measure Performance")
    st.dataframe(
        [
            {
                "Measure": result.measure_id,
                "Denominator": result.denominator_count,
                "Numerator": result.numerator_count,
                "Rate": round(result.performance_rate, 3),
            }
            for result in results
        ],
        use_container_width=True,
    )

    st.subheader("Care Gap Worklist")
    st.dataframe([gap.__dict__ for gap in gaps], use_container_width=True)
