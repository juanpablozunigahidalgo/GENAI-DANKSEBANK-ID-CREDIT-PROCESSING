from fastapi import APIRouter

router = APIRouter(prefix="/customer")

@router.post("/")
def create_customer():
    return {"message": "Customer created (mocked)."}
