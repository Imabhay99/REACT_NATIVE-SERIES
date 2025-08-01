from fastapi import APIRouter, UploadFile, File
import cloudinary.uploader
from app.services.virtual_tryon_service import (
    upload_and_generate_tryon,
    process_virtual_tryon,
    get_look_completion
)
from app.schemas.tryon_schemas import TryOnResponse
from app.schemas.complete_look_response import CompleteLookResponse

router = APIRouter()

@router.post("/test")
async def test_upload(file: UploadFile = File(...)):
    result = cloudinary.uploader.upload(file.file)
    return {"url": result["secure_url"]}

@router.post("/upload", response_model=TryOnResponse)
async def upload_tryon(user_image: UploadFile = File(...), clothing_image: UploadFile = File(...)):
    return await upload_and_generate_tryon(user_image, clothing_image)

@router.post("/virtual-try-on", response_model=TryOnResponse)
async def generate_virtual_tryon(user_image_url: str, clothing_image_url: str):
    return await process_virtual_tryon(user_image_url, clothing_image_url)

@router.post("/generate_complete_look", response_model=CompleteLookResponse)
async def get_recommendation(clothing_id: str):
    return await get_look_completion(clothing_id)
