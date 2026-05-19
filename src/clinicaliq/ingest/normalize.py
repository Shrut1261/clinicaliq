from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from clinicaliq.fhir.models import (
    ConditionResource,
    ImmunizationResource,
    MedicationRequestResource,
    ObservationResource,
    PatientResource,
    ProcedureResource,
)


@dataclass(frozen=True)
class ClinicalEvent:
    code: str
    system: str | None = None
    display: str | None = None
    date: date | None = None
    value: float | None = None
    unit: str | None = None


@dataclass
class PatientRecord:
    patient_id: str
    birth_date: date | None
    sex: str | None
    conditions: list[ClinicalEvent] = field(default_factory=list)
    observations: list[ClinicalEvent] = field(default_factory=list)
    procedures: list[ClinicalEvent] = field(default_factory=list)
    immunizations: list[ClinicalEvent] = field(default_factory=list)
    medications: list[ClinicalEvent] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def _first_code(resource_code: object) -> tuple[str, str | None, str | None]:
    coding = getattr(resource_code, "first_code", None)
    if coding is None or coding.code is None:
        return ("UNKNOWN", None, getattr(resource_code, "text", None))
    return (coding.code, coding.system, coding.display)


def normalize_resources(resources: list[object]) -> dict[str, PatientRecord]:
    patients: dict[str, PatientRecord] = {}
    for resource in resources:
        if isinstance(resource, PatientResource):
            patients[resource.id] = PatientRecord(
                patient_id=resource.id,
                birth_date=resource.birthDate,
                sex=resource.gender,
            )

    for resource in resources:
        if isinstance(resource, ConditionResource):
            record = patients.setdefault(
                resource.subject.resource_id,
                PatientRecord(resource.subject.resource_id, None, None),
            )
            code, system, display = _first_code(resource.code)
            record.conditions.append(ClinicalEvent(code, system, display, resource.onsetDateTime))
        elif isinstance(resource, ObservationResource):
            record = patients.setdefault(
                resource.subject.resource_id,
                PatientRecord(resource.subject.resource_id, None, None),
            )
            code, system, display = _first_code(resource.code)
            value = None
            unit = None
            if resource.valueQuantity:
                raw_value = resource.valueQuantity.get("value")
                value = float(raw_value) if raw_value is not None else None
                unit = resource.valueQuantity.get("unit")
            record.observations.append(
                ClinicalEvent(code, system, display, resource.effectiveDateTime, value, unit)
            )
        elif isinstance(resource, ProcedureResource):
            record = patients.setdefault(
                resource.subject.resource_id,
                PatientRecord(resource.subject.resource_id, None, None),
            )
            code, system, display = _first_code(resource.code)
            record.procedures.append(
                ClinicalEvent(code, system, display, resource.performedDateTime)
            )
        elif isinstance(resource, ImmunizationResource):
            record = patients.setdefault(
                resource.patient.resource_id,
                PatientRecord(resource.patient.resource_id, None, None),
            )
            code, system, display = _first_code(resource.vaccineCode)
            record.immunizations.append(
                ClinicalEvent(code, system, display, resource.occurrenceDateTime)
            )
        elif isinstance(resource, MedicationRequestResource):
            record = patients.setdefault(
                resource.subject.resource_id,
                PatientRecord(resource.subject.resource_id, None, None),
            )
            codeable = resource.medicationCodeableConcept
            if codeable is not None:
                code, system, display = _first_code(codeable)
                record.medications.append(ClinicalEvent(code, system, display, resource.authoredOn))
    return patients
