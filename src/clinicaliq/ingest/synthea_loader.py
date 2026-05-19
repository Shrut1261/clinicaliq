from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from clinicaliq.fhir.validator import validate_bundle, validate_resource
from clinicaliq.logging import audit_event


def load_bundle(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    typed_payload = cast(dict[str, Any], payload)
    validate_bundle(typed_payload)
    audit_event("fhir_bundle_loaded", path=str(path), entries=len(payload.get("entry", [])))
    return typed_payload


def iter_resources(bundle: dict[str, Any]) -> list[object]:
    resources: list[object] = []
    for entry in bundle.get("entry", []):
        resource = entry.get("resource", {})
        if resource.get("resourceType") in {
            "Patient",
            "Condition",
            "Observation",
            "Procedure",
            "Immunization",
            "MedicationRequest",
        }:
            resources.append(validate_resource(resource))
    return resources
