# backend/services/id_verification/norway.py
from typing import Dict, Any

# Simulated Norwegian National Registry (Folkeregisteret) keyed by fødselsnummer
NO_FOLKEREGISTER: Dict[str, Dict[str, Any]] = {
    "47010112345": {
        "firstName": "Ola",
        "lastName": "Nordmann",
        "dateOfBirth": "2001-01-01",
        "gender": "male",
        "address": "Karl Johans gate 1, 0154 Oslo",
        "maritalStatus": "single",
        "citizenship": ["Norway"],
    },
    "47020254321": {
        "firstName": "Kari",
        "lastName": "Nordmann",
        "dateOfBirth": "2002-02-02",
        "gender": "female",
        "address": "Bygdøy allé 20, 0262 Oslo",
        "maritalStatus": "married",
        "citizenship": ["Norway"],
    },
}


def verify_norway_registry(national_id: str) -> Dict[str, Any]:
    """
    Simulated Norwegian Folkeregister lookup.
    Approves ONLY if national_id exists in NO_FOLKEREGISTER.
    """
    if not national_id:
        return {
            "status": "rejected",
            "reason": "No Norwegian national id provided.",
            "registry_record": None,
            "source": "norway",
        }

    fodselsnummer = national_id.strip()
    person = NO_FOLKEREGISTER.get(fodselsnummer)

    if not person:
        return {
            "status": "rejected",
            "reason": f"Norwegian id {fodselsnummer} not found in registry (mock).",
            "registry_record": None,
            "source": "norway",
        }

    registry_record = {
        "national_id": fodselsnummer,
        **person,
    }

    return {
        "status": "approved",
        "reason": "Found in Norwegian registry (mock).",
        "registry_record": registry_record,
        "source": "norway",
    }
