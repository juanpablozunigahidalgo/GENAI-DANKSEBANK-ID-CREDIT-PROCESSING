# backend/services/id_verification/denmark.py
from typing import Dict, Any, List

# Simulated CPR registry (keyed by CPR number)
DK_CPR_REGISTRY: Dict[str, Dict[str, Any]] = {
    "123456-7890": {
        "firstName": "John",
        "lastName": "Doe",
        "dateOfBirth": "1985-04-12",
        "gender": "male",
        "address": "POC Street 1, 2100 Copenhagen",
        "maritalStatus": "married",
        "citizenship": ["Denmark"],
    },
    "160778-1234": {
        "firstName": "Maria",
        "lastName": "Larsen",
        "dateOfBirth": "1978-07-16",
        "gender": "female",
        "address": "Hovedgaden 10, 8000 Aarhus",
        "maritalStatus": "single",
        "citizenship": ["Denmark"],
    },
    # add more CPRs here if needed
}


def verify_denmark_cpr(national_id: str) -> Dict[str, Any]:
    """
    Simulated Det Centrale Personregister (CPR) lookup.
    GET /oplysninger/{cprNumber}
    Returns person data if CPR exists.
    """
    if not national_id:
        return {
            "status": "rejected",
            "reason": "No CPR provided.",
            "registry_record": None,
            "source": "denmark",
        }

    cpr_number = national_id.strip()
    person = DK_CPR_REGISTRY.get(cpr_number)

    if not person:
        return {
            "status": "rejected",
            "reason": f"CPR {cpr_number} not found in Danish CPR (mock).",
            "registry_record": None,
            "source": "denmark",
        }

    # echo back the ID and include registry data
    registry_record = {
        "national_id": cpr_number,
        **person,
    }

    return {
        "status": "approved",
        "reason": "CPR found in Danish CPR (mock).",
        "registry_record": registry_record,
        "source": "denmark",
    }
