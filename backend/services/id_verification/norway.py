# backend/services/id_verification/norway.py
from typing import Dict, Any


def verify_norway_registry(national_id: str) -> Dict[str, Any]:
    """
    POC for Norwegian Folkeregister.
    """
    status = "rejected"
    reason = "Not found in Norwegian registry (POC)."
    record = None

    if national_id and national_id.startswith("47"):
        status = "approved"
        reason = "Matched Norwegian registry (POC)."
        record = {
            "first_name": "Ola",
            "last_name": "Nordmann",
            "address": "Karl Johans gate 1, Oslo",
            "citizenship": "Norway",
        }

    return {
        "status": status,
        "reason": reason,
        "registry_record": record,
        "source": "norway",
    }
