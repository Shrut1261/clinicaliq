from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ClinicalEntity:
    text: str
    label: str
    negated: bool = False


PROBLEM_TERMS = {
    "diabetes": "PROBLEM",
    "hypertension": "PROBLEM",
    "asthma": "PROBLEM",
    "depression": "PROBLEM",
}
SDOH_TERMS = {
    "homeless": "SDOH_HOUSING",
    "food insecurity": "SDOH_FOOD",
    "transportation barrier": "SDOH_TRANSPORTATION",
}


def extract_entities(note: str) -> list[ClinicalEntity]:
    """Rule-based NLP fallback used when scispaCy models are not installed."""
    lower = note.lower()
    entities: list[ClinicalEntity] = []
    for term, label in {**PROBLEM_TERMS, **SDOH_TERMS}.items():
        if term in lower:
            prefix = lower[max(0, lower.find(term) - 12) : lower.find(term)]
            entities.append(ClinicalEntity(text=term, label=label, negated="no " in prefix))
    return entities
