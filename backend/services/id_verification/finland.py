# backend/services/id_verification/finland.py
from typing import Dict, Any

# Simulated Finnish Population Information System (Väestötietojärjestelmä)
# keyed by Finnish personal identity code
FI_POPULATION_REGISTRY: Dict[str, Dict[str, Any]] = {
    "FI-120394-123X": {
        "firstName": "Matti",
        "lastName": "Korhonen",
        "dateOfBirth": "1994-03-12",
        "gender": "male",
        "address": "Mannerheimintie 10, 00100 Helsinki",
        "maritalStatus": "married",
        "citizenship": ["Finland"],
    },
    "FI-010180-999Y": {
        "firstName": "Liisa",
        "lastName": "Virtanen",
        "dateOfBirth": "1980-01-01",
        "gender": "female",
        "address": "Hämeenkatu 5, 33100 Tampere",
        "maritalStatus": "single",
        "citizenship": ["Finland"],
    },
}


def verify_finland_registry(national_id: str) -> Dict[str, Any]:
    """
    Simulated Finnish registry lookup.
    Approves ONLY if national_id exists in FI_POPULATION_REGISTRY.
    """
    if not national_id:
        return {
            "status": "rejected",
            "reason": "No Finnish id provided.",
            "registry_record": None,
            "source": "finland",
        }

    hetu = national_id.strip()
    person = FI_POPULATION_REGISTRY.get(hetu)

    if not person:
        return {
            "status": "rejected",
            "reason": f"Finnish id {hetu} not found in registry (mock).",
            "registry_record": None,
            "source": "finland",
        }

    registry_record = {
        "national_id": hetu,
        **person,
    }

    return {
        "status": "approved",
        "reason": "Found in Finnish registry (mock).",
        "registry_record": registry_record,
        "source": "finland",
    }
