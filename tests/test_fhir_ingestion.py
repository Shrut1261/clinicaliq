from __future__ import annotations

from clinicaliq.fhir.validator import validate_bundle
from clinicaliq.ingest.normalize import normalize_resources
from clinicaliq.ingest.synthea_loader import iter_resources


def test_bundle_validation_and_normalization() -> None:
    bundle = {
        "resourceType": "Bundle",
        "id": "bundle-1",
        "entry": [
            {
                "resource": {
                    "resourceType": "Patient",
                    "id": "p1",
                    "birthDate": "1970-01-01",
                    "gender": "female",
                }
            },
            {
                "resource": {
                    "resourceType": "Condition",
                    "id": "c1",
                    "subject": {"reference": "Patient/p1"},
                    "code": {"coding": [{"system": "SNOMED", "code": "44054006"}]},
                    "onsetDateTime": "2020-01-01",
                }
            },
            {
                "resource": {
                    "resourceType": "Observation",
                    "id": "o1",
                    "subject": {"reference": "Patient/p1"},
                    "code": {"coding": [{"system": "LOINC", "code": "4548-4"}]},
                    "effectiveDateTime": "2026-01-01",
                    "valueQuantity": {"value": 7.4, "unit": "%"},
                }
            },
        ],
    }

    validate_bundle(bundle)
    records = normalize_resources(iter_resources(bundle))

    assert records["p1"].sex == "female"
    assert records["p1"].conditions[0].code == "44054006"
    assert records["p1"].observations[0].value == 7.4
