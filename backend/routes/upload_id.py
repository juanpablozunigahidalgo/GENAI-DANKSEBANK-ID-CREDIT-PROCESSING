from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import uuid
import os
from pathlib import Path


router = APIRouter(prefix="/upload-id")
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/")
async def upload_id_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    save_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
    with open(save_path, "wb") as buffer:
        buffer.write(await file.read())

    # Mocked CPR verification response:
    verified_user = {
        "name": "John Doe",
        "cpr": "123456-7890",
        "country": "Denmark",
        "status": "Verified"
    }

    return JSONResponse(content={
        "upload_status": "success",
        "file_path": str(save_path),
        "verified_user": verified_user
    })
