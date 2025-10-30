# routes/cpr_registry.py
from fastapi import APIRouter

router = APIRouter(prefix="/cpr")

@router.get("/{cpr_id}")
def get_cpr_data(cpr_id: str):
    return {
        "name": "John Doe",
        "cpr_id": cpr_id,
        "status": "Mocked lookup OK"
    }
