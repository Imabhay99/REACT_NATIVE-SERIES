from fastapi import UploadFile
from app.services.model_service import (
    process_virtual_tryon,
    get_look_completion,
    upload_and_generate_tryon
)

async def virtual_try_on(user_image_url: str, clothing_image_url: str):
    return await process_virtual_tryon(user_image_url, clothing_image_url)

async def complete_the_look(clothing_id: str):
    return await get_look_completion(clothing_id)

async def generate_tryon_image(user_image: UploadFile, clothing_image: UploadFile):
    return await upload_and_generate_tryon(user_image, clothing_image)
