from pydantic import BaseModel

class TryOnResponse(BaseModel):
    tryon_image_url: str
