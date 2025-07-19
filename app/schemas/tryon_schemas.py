from pydantic import BaseModel

class TryOnInput(BaseModel):
    user_image_url: str
    cloth_image_url: str

class TryOnResponse(BaseModel):
    tryon_image_url: str
