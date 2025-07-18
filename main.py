import sys
import os
from fastapi import FastAPI
from app.routers.virtual_tryon_router import router as virtual_tryon_router
from app.routers.inference_router import router as inference_router
from app.routers.training_router import router as training_router
from app.routers.virtual_tryon_router import router as virtual_tryon_router

app = FastAPI()


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app.include_router(virtual_tryon_router, prefix="/tryon", tags=["Virtual Try-On"])
app.include_router(inference_router, prefix="/inference", tags=["Inference"])
app.include_router(training_router, prefix="/training", tags=["Training"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Virtual Try-On API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("able_app.main:app", host="127.0.0.1", port=8000, reload=True)


