from fastapi import APIRouter, UploadFile, File, HTTPException
from app.controllers.training_controller import upload_clothing_item, get_all_clothing_items

router = APIRouter(prefix="/train", tags=["Training"])

@router.post("/upload")
async def upload(file: UploadFile = File(...), size: str = "M"):
    try:
        return await upload_clothing_item(file, size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clothing-items")
async def fetch_clothing_items():
    try:
        return await get_all_clothing_items()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
