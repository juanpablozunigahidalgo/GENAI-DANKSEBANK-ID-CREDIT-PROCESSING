# backend/services/id_verification/sweden.py
from typing import Dict, Any


def verify_sweden_spar(national_id: str) -> Dict[str, Any]:
    """
    POC SPAR check for Sweden.
    """
    status = "rejected"
    reason = "Not found in Swedish SPAR (POC)."
    record = None

    if national_id and national_id.endswith("0"):
        status = "approved"
        reason = "Matched Swedish SPAR (POC)."
        record = {
            "first_name": "Anna",
            "last_name": "Svensson",
            "address": "Storgatan 1, Stockholm",
            "citizenship": "Sweden",
        }

    return {
        "status": status,
        "reason": reason,
        "registry_record": record,
        "source": "sweden",
    }
