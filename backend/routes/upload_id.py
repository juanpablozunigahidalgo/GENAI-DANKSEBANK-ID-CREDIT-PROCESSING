# backend/routes/upload_id.py
from fastapi import APIRouter, File, UploadFile, Query
from fastapi.responses import JSONResponse
import uuid
from pathlib import Path
import httpx

from backend.utils.tools import UPLOADED_IDS

router = APIRouter(prefix="/upload-id", tags=["default"])
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/")
async def upload_id_file(
    file: UploadFile = File(...),
    user_id: str = Query(..., description="Same user_id used in /chat"),
):
    # 1) save file
    file_id = str(uuid.uuid4())
    save_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
    with open(save_path, "wb") as buffer:
        buffer.write(await file.read())

    # 2) OCR mock (realistic, like the CPR DB)
    parsed_id = {
        "firstName": "John",
        "lastName": "Doe",
        "dateOfBirth": "1985-04-12",
        "gender": "male",
        "address": "POC Street 1, 2100 Copenhagen",
        "maritalStatus": "married",
        "citizenship": ["Denmark"],
        "national_id": "123456-7890",
        "country": "Denmark",

        # snake_case for agent compatibility
        "first_name": "John",
        "last_name": "Doe",

        "file_path": str(save_path),
    }

    national_id = parsed_id["national_id"]
    country = parsed_id["country"]

    # 3) call central registry API (same app)
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "http://127.0.0.1:8000/registry/",
            params={"national_id": national_id, "country": country},
        )
    registry_resp = resp.json()

    # 4) map registry response -> internal "verification" structure
    # so the agent sees the SAME shape as before
    if registry_resp.get("status") == "found":
        verification_result = {
            "status": "approved",
            "reason": registry_resp.get("message", "Found in national registry."),
            "registry_record": registry_resp.get("registry_record") or {},
            "source": registry_resp.get("source") or country.lower(),
        }
    else:
        verification_result = {
            "status": "rejected",
            "reason": registry_resp.get("message", "Not found in national registry."),
            "registry_record": None,
            "source": registry_resp.get("source") or country.lower(),
        }

    # 5) extra safety: OCR ID must match registry ID
    registry_id = (verification_result.get("registry_record") or {}).get("national_id")
    if verification_result["status"] == "approved":
        if not registry_id or registry_id != national_id:
            verification_result["status"] = "rejected"
            verification_result["reason"] = "ID mismatch between OCR and national registry."

    # 6) store FULL object for the agent
    UPLOADED_IDS[user_id] = {
        **parsed_id,
        "verification": verification_result,
    }

    # 7) return short response to client
    return JSONResponse(
        content={
            "upload_status": "success",
            "user_id": user_id,
            "parsed_id": parsed_id,              # puedes quitarlo si lo quieres corto
            "verification": verification_result, # el agente espera esto
        }
    )
