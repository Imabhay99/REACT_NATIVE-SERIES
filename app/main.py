from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.virtual_tryon_router import router as virtual_tryon_router

app = FastAPI(
    title="Virtual Try-On API",
    version="1.0.0",
    description="API for virtual try-on and fashion recommendations"
)

# Optional: CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register router
app.include_router(virtual_tryon_router, prefix="/api/tryon", tags=["Virtual Try-On"])

# Root route
@app.get("/")
def read_root():
    return {"message": "Virtual Try-On API is running!"}
