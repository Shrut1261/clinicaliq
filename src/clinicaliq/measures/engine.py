from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol

from clinicaliq.ingest.normalize import PatientRecord


@dataclass(frozen=True)
class MeasureResult:
    measure_id: str
    denominator: list[str]
    numerator: list[str]
    exclusions: list[str]

    @property
    def denominator_count(self) -> int:
        return len(self.denominator)

    @property
    def numerator_count(self) -> int:
        return len(self.numerator)

    @property
    def performance_rate(self) -> float:
        if self.denominator_count == 0:
            return 0.0
        return self.numerator_count / self.denominator_count


class QualityMeasure(Protocol):
    measure_id: str

    def evaluate(self, patients: list[PatientRecord], as_of: date) -> MeasureResult: ...


def age_on(birth_date: date | None, as_of: date) -> int | None:
    if birth_date is None:
        return None
    return (
        as_of.year
        - birth_date.year
        - ((as_of.month, as_of.day) < (birth_date.month, birth_date.day))
    )


def within_years(event_date: date | None, as_of: date, years: int) -> bool:
    if event_date is None:
        return False
    return 0 <= (as_of - event_date).days <= years * 365


def run_measures(
    measures: list[QualityMeasure], patients: list[PatientRecord], as_of: date
) -> list[MeasureResult]:
    return [measure.evaluate(patients, as_of) for measure in measures]
