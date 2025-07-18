from fastapi import APIRouter, UploadFile, File, HTTPException
from app.controllers.inference_controller import (
    virtual_try_on,
    complete_the_look,
    generate_tryon_image
)

router = APIRouter(prefix="/inference", tags=["Inference"])


@router.post("/virtual-try-on")
async def try_on(user_image_url: str, clothing_image_url: str):
    try:
        return await virtual_try_on(user_image_url, clothing_image_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/complete-the-look")
async def complete_look(clothing_id: str):
    try:
        return await complete_the_look(clothing_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tryon-image")
async def tryon_image(user_image: UploadFile = File(...), clothing_image: UploadFile = File(...)):
    try:
        return await generate_tryon_image(user_image, clothing_image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


