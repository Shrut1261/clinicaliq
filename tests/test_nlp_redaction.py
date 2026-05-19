from __future__ import annotations

from clinicaliq.logging import redact_phi
from clinicaliq.nlp.rules import extract_entities


def test_rule_based_nlp_extracts_problem_and_sdoh() -> None:
    entities = extract_entities("Patient has diabetes and reports food insecurity.")
    labels = {entity.label for entity in entities}

    assert "PROBLEM" in labels
    assert "SDOH_FOOD" in labels


def test_phi_redaction_removes_email_and_address_fields() -> None:
    redacted = redact_phi({"name": "Jane Doe", "note": "call jane@example.com"})

    assert redacted["name"] == "[REDACTED]"
    assert redacted["note"] == "call [REDACTED_EMAIL]"
