# routes/health.py
from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def root():
    return {"status": "OK", "message": "Backend is alive"}