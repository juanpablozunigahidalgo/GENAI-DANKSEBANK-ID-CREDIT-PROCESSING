# backend/services/id_verification/denmark.py
from typing import Dict, Any


def verify_denmark_cpr(national_id: str) -> Dict[str, Any]:
    """
    POC CPR check for Denmark.
    Real version would call CPR API.
    Here we do a deterministic mock: even → approved, odd → rejected.
    """
    status = "rejected"
    reason = "Not found in Danish CPR (POC)."
    record = None

    if national_id:
        last = national_id.strip()[-1]
        if last.isdigit() and int(last) % 2 == 0:
            status = "approved"
            reason = "Matched Danish CPR (POC)."
            record = {
                "first_name": "John",
                "last_name": "Doe",
                "address": "POC Street 1, Copenhagen",
                "citizenship": "Denmark",
            }

    return {
        "status": status,
        "reason": reason,
        "registry_record": record,
        "source": "denmark",
    }
