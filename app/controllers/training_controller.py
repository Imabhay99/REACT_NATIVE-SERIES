from fastapi import UploadFile
from app.services.dataset_service import save_clothing_item, get_clothing_items

async def upload_clothing_item(file: UploadFile, size: str):
    # Save file and metadata (size)
    return await save_clothing_item(file, size)

async def get_all_clothing_items():
    return await get_clothing_items()
