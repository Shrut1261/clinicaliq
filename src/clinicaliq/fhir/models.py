from __future__ import annotations

from datetime import date
from typing import Any, Literal

from pydantic import BaseModel, Field


class FHIRReference(BaseModel):
    reference: str

    @property
    def resource_id(self) -> str:
        return self.reference.split("/")[-1]


class Coding(BaseModel):
    system: str | None = None
    code: str | None = None
    display: str | None = None


class CodeableConcept(BaseModel):
    coding: list[Coding] = Field(default_factory=list)
    text: str | None = None

    @property
    def first_code(self) -> Coding | None:
        return self.coding[0] if self.coding else None


class PatientResource(BaseModel):
    resourceType: Literal["Patient"]
    id: str
    birthDate: date | None = None
    gender: str | None = None
    extension: list[dict[str, Any]] = Field(default_factory=list)
    address: list[dict[str, Any]] = Field(default_factory=list)


class ConditionResource(BaseModel):
    resourceType: Literal["Condition"]
    id: str
    subject: FHIRReference
    code: CodeableConcept = Field(default_factory=CodeableConcept)
    onsetDateTime: date | None = None


class ObservationResource(BaseModel):
    resourceType: Literal["Observation"]
    id: str
    subject: FHIRReference
    code: CodeableConcept = Field(default_factory=CodeableConcept)
    effectiveDateTime: date | None = None
    valueQuantity: dict[str, Any] | None = None
    component: list[dict[str, Any]] = Field(default_factory=list)


class ProcedureResource(BaseModel):
    resourceType: Literal["Procedure"]
    id: str
    subject: FHIRReference
    code: CodeableConcept = Field(default_factory=CodeableConcept)
    performedDateTime: date | None = None


class ImmunizationResource(BaseModel):
    resourceType: Literal["Immunization"]
    id: str
    patient: FHIRReference
    vaccineCode: CodeableConcept = Field(default_factory=CodeableConcept)
    occurrenceDateTime: date | None = None


class MedicationRequestResource(BaseModel):
    resourceType: Literal["MedicationRequest"]
    id: str
    subject: FHIRReference
    medicationCodeableConcept: CodeableConcept | None = None
    authoredOn: date | None = None


FHIRResource = (
    PatientResource
    | ConditionResource
    | ObservationResource
    | ProcedureResource
    | ImmunizationResource
    | MedicationRequestResource
)


class BundleEntry(BaseModel):
    resource: dict[str, Any]


class BundleResource(BaseModel):
    resourceType: Literal["Bundle"]
    id: str | None = None
    type: str | None = None
    entry: list[BundleEntry] = Field(default_factory=list)
