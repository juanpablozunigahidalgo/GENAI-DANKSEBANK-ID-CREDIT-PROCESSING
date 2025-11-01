# backend/services/id_verification/sweden.py
from typing import Dict, Any

# Simulated SPAR / Swedish population registry (keyed by personal number)
SE_SPAR_REGISTRY: Dict[str, Dict[str, Any]] = {
    "19800101-1230": {
        "firstName": "Anna",
        "lastName": "Svensson",
        "dateOfBirth": "1980-01-01",
        "gender": "female",
        "address": "Storgatan 1, 111 22 Stockholm",
        "maritalStatus": "married",
        "citizenship": ["Sweden"],
    },
    "19950715-8899": {
        "firstName": "Erik",
        "lastName": "Johansson",
        "dateOfBirth": "1995-07-15",
        "gender": "male",
        "address": "Västra Hamngatan 5, 411 17 Göteborg",
        "maritalStatus": "single",
        "citizenship": ["Sweden"],
    },
}


def verify_sweden_spar(national_id: str) -> Dict[str, Any]:
    """
    Simulated Swedish registry/SPAR lookup.
    Approves ONLY if national_id exists in SE_SPAR_REGISTRY.
    """
    if not national_id:
        return {
            "status": "rejected",
            "reason": "No Swedish personal number provided.",
            "registry_record": None,
            "source": "sweden",
        }

    personal_number = national_id.strip()
    person = SE_SPAR_REGISTRY.get(personal_number)

    if not person:
        return {
            "status": "rejected",
            "reason": f"Swedish personal number {personal_number} not found in SPAR (mock).",
            "registry_record": None,
            "source": "sweden",
        }

    registry_record = {
        "national_id": personal_number,
        **person,
    }

    return {
        "status": "approved",
        "reason": "Found in Swedish SPAR (mock).",
        "registry_record": registry_record,
        "source": "sweden",
    }
