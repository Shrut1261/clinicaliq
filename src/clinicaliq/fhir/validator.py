from __future__ import annotations

from typing import Any, cast

from pydantic import BaseModel, ValidationError

from clinicaliq.fhir.models import (
    BundleResource,
    ConditionResource,
    ImmunizationResource,
    MedicationRequestResource,
    ObservationResource,
    PatientResource,
    ProcedureResource,
)

RESOURCE_MODELS: dict[str, type[BaseModel]] = {
    "Patient": PatientResource,
    "Condition": ConditionResource,
    "Observation": ObservationResource,
    "Procedure": ProcedureResource,
    "Immunization": ImmunizationResource,
    "MedicationRequest": MedicationRequestResource,
}


class FHIRValidationError(ValueError):
    pass


def validate_bundle(payload: dict[str, Any]) -> BundleResource:
    try:
        return BundleResource.model_validate(payload)
    except ValidationError as exc:
        raise FHIRValidationError("Invalid FHIR Bundle structure") from exc


def validate_resource(payload: dict[str, Any]) -> object:
    resource_type = cast(str | None, payload.get("resourceType"))
    if resource_type is None:
        raise FHIRValidationError("FHIR resource missing resourceType")
    model = RESOURCE_MODELS.get(resource_type)
    if model is None:
        raise FHIRValidationError(f"Unsupported FHIR resource type: {resource_type}")
    try:
        return model.model_validate(payload)
    except ValidationError as exc:
        raise FHIRValidationError(f"Invalid FHIR resource: {resource_type}") from exc
