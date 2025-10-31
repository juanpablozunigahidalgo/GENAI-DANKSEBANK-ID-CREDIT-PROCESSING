# backend/services/id_verification/finland.py
from typing import Dict, Any


def verify_finland_registry(national_id: str) -> Dict[str, Any]:
    """
    POC for Finnish Population Information System.
    """
    status = "rejected"
    reason = "Not found in Finnish registry (POC)."
    record = None

    if national_id and "FI" in national_id.upper():
        status = "approved"
        reason = "Matched Finnish registry (POC)."
        record = {
            "first_name": "Matti",
            "last_name": "Korhonen",
            "address": "Helsinki 00100",
            "citizenship": "Finland",
        }

    return {
        "status": status,
        "reason": reason,
        "registry_record": record,
        "source": "finland",
    }
