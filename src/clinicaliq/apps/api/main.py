from __future__ import annotations

from datetime import date

from fastapi import FastAPI

from clinicaliq.care_gaps.identifier import identify_care_gaps
from clinicaliq.measures.catalog import DEFAULT_MEASURES
from clinicaliq.sample_data import sample_patients

app = FastAPI(title="ClinicalIQ API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/measures")
def measures() -> list[dict[str, object]]:
    patients = sample_patients()
    return [
        {
            "measure_id": result.measure_id,
            "denominator": result.denominator_count,
            "numerator": result.numerator_count,
            "performance_rate": round(result.performance_rate, 4),
        }
        for result in [
            measure.evaluate(patients, date(2026, 12, 31)) for measure in DEFAULT_MEASURES
        ]
    ]


@app.get("/care-gaps")
def care_gaps() -> list[dict[str, str]]:
    patients = sample_patients()
    return [
        gap.__dict__ for gap in identify_care_gaps(patients, DEFAULT_MEASURES, date(2026, 12, 31))
    ]
