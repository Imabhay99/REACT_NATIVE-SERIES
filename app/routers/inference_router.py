from fastapi import APIRouter, File, UploadFile
import uuid
import os
import shutil
from controllers.inference_controller import FashionController
from config.cloudinary_config import cloudinary

router = APIRouter()
controller = FashionController()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        result = cloudinary.uploader.upload(file.file)
        return {
            "message": "Upload successful",
            "url": result.get("secure_url")
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/clothing-items", response_model=list[ClothingItemSchema])
async def get_clothing_items():
    return controller.get_clothing_items()

@router.post("/virtual-try-on", response_model=TryOnResponse)
async def virtual_try_on(request: VirtualTryOnRequest):
    return controller.generate_try_on_image(request)

@router.post("/complete-the-look", response_model=CompleteLookResponse)
async def complete_the_look(request: CompleteLookRequest):
    return controller.get_complete_look(request)

@router.post("/tryon-image")
async def tryon_image(user_image: UploadFile = File(...), clothing_image: UploadFile = File(...)):
    try:
        user_path = os.path.join(UPLOAD_DIR, f"user_{uuid.uuid4().hex}.jpg")
        cloth_path = os.path.join(UPLOAD_DIR, f"cloth_{uuid.uuid4().hex}.jpg")

        with open(user_path, "wb") as f:
            shutil.copyfileobj(user_image.file, f)

        with open(cloth_path, "wb") as f:
            shutil.copyfileobj(clothing_image.file, f)

        result_url = run_inference(user_path, cloth_path)

        return {"tryon_image_url": result_url}
    except Exception as e:
        return {"error": str(e)}
