# backend/routes/upload_id.py
from fastapi import APIRouter, File, UploadFile, Query
from fastapi.responses import JSONResponse
import uuid
from pathlib import Path

from backend.utils.tools import UPLOADED_IDS
from backend.services.id_verification.engine import verify_identity  # 👈 explicit import

router = APIRouter(prefix="/upload-id", tags=["default"])
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/")
async def upload_id_file(
    file: UploadFile = File(...),
    user_id: str = Query(..., description="Same user_id used in /chat"),
    simulate: str = Query(None, description="force approve/reject for POC"),
):
    # 1) save file
    file_id = str(uuid.uuid4())
    save_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
    with open(save_path, "wb") as buffer:
        buffer.write(await file.read())

    # 2) mock OCR result
    parsed_id = {
        "first_name": "John",
        "last_name": "Doe",
        "national_id": "123456-7890",
        "country": "Denmark",
        "status": "Verified",
        "file_path": str(save_path),
    }

    # 3) call independent verification engine
    verification_result = verify_identity(
        parsed_id.get("national_id", ""),
        parsed_id.get("country", "Denmark"),
    )

    # 4) allow manual override
    if simulate:
        if simulate.lower() == "approve":
            verification_result["status"] = "approved"
            verification_result["reason"] = "Simulated approval (forced)."
        elif simulate.lower() == "reject":
            verification_result["status"] = "rejected"
            verification_result["reason"] = "Simulated rejection (forced)."

    # 5) store for agent
    UPLOADED_IDS[user_id] = {
        **parsed_id,
        "verification": verification_result,
    }

    # 6) return to caller
    return JSONResponse(
        content={
            "upload_status": "success",
            "user_id": user_id,
            "parsed_id": parsed_id,
            "verification": verification_result,
        }
    )
