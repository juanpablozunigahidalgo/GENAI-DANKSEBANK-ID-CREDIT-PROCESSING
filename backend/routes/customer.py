from fastapi import APIRouter

router = APIRouter(prefix="/customer", tags=["customer"])

@router.post("/")
def create_customer():
    # Aquí en el futuro podrías llamar al "customer api.yaml"
    return {"message": "Customer created (mocked)."}
