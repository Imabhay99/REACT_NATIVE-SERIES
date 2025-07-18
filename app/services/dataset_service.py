import os
from fastapi import UploadFile
from app.schemas.clothing_item import ClothingItemSchema
# from app.database import clothing_collection  # MongoDB collection

async def save_clothing_item(file: UploadFile, size: str):
    filename = file.filename
    file_location = f"static/clothing/{filename}"

    # Save file to local folder
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Insert into DB
    item_data = {
        "filename": filename,
        "size": size,
        "path": file_location,
    }

    result = await clothing_collection.insert_one(item_data)
    return {"id": str(result.inserted_id), **item_data}

async def get_clothing_items():
    items = []
    async for item in clothing_collection.find():
        items.append(ClothingItemSchema(**item))
    return items
