# backend/routes/customer.py
from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter(prefix="/customer", tags=["customer"])

DB_FILE = Path("data/customers.json")

@router.get("/all")
def list_customers():
    """Return all customers saved by the onboarding agent (POC)."""
    if not DB_FILE.exists():
        return []
    return json.loads(DB_FILE.read_text(encoding="utf-8"))
