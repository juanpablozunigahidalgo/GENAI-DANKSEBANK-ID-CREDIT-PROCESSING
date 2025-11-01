# backend/routes/cpr_registry.py
from fastapi import APIRouter, Query
from backend.services.id_verification.engine import verify_identity

router = APIRouter(prefix="/registry", tags=["registry"])


@router.get("/")
def check_national_registry(
    national_id: str = Query(..., description="National ID / CPR / personal number"),
    country: str = Query(..., description="Country name or code (Denmark, Sweden, Norway, Finland)")
):
    """
    Central registry API mock.

    Simulates a real Nordic cross-country verification service.
    Calls the engine, which routes to the specific country's registry mock.
    """

    verification = verify_identity(national_id, country)
    status = verification.get("status", "unknown")

    if status == "approved":
        return {
            "national_id": national_id,
            "country": country,
            "status": "found",
            "registry_record": verification.get("registry_record", {}),
            "source": verification.get("source"),
            "message": "Person found in national registry (mock).",
        }
    elif status == "rejected":
        return {
            "national_id": national_id,
            "country": country,
            "status": "not_found",
            "registry_record": None,
            "source": verification.get("source"),
            "message": verification.get("reason", "Person not found in registry."),
        }
    else:
        return {
            "national_id": national_id,
            "country": country,
            "status": "error",
            "message": "Unexpected response from engine.",
        }
