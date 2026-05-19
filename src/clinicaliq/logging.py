from __future__ import annotations

import re
from typing import Any

from loguru import logger

PHI_KEYS = {"name", "given", "family", "telecom", "address", "ssn", "mrn"}
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")


def redact_phi(value: Any) -> Any:
    """Redact obvious PHI-like fields before logging.

    This project uses synthetic data, but production clinical systems must avoid
    writing patient identifiers into logs, exceptions, metrics, or traces.
    """
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if key.lower() in PHI_KEYS else redact_phi(child)
            for key, child in value.items()
        }
    if isinstance(value, list):
        return [redact_phi(child) for child in value]
    if isinstance(value, str):
        return PHONE_RE.sub("[REDACTED_PHONE]", EMAIL_RE.sub("[REDACTED_EMAIL]", value))
    return value


def audit_event(event: str, **fields: Any) -> None:
    logger.bind(event=event).info("{event} {fields}", event=event, fields=redact_phi(fields))
