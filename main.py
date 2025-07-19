import sys
import os
from fastapi import FastAPI

# Adjust the import paths according to the repository structure
from app.routers.virtual_tryon_router import router as virtual_tryon_router
from app.routers.inference_router import router as inference_router
from app.routers.training_router import router as training_router

app = FastAPI()

# Ensure the app can find the modules in the app directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Include routers with appropriate prefixes and tags
app.include_router(virtual_tryon_router, prefix="/tryon", tags=["Virtual Try-On"])
app.include_router(inference_router, prefix="/inference", tags=["Inference"])
app.include_router(training_router, prefix="/training", tags=["Training"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Virtual Try-On API!"}

if __name__ == "__main__":
    import uvicorn
    # Correct the module path to match the structure
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
