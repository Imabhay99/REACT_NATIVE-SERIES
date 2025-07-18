from pydantic import BaseModel
from enum import Enum

class SizeEnum(str, Enum):
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"

class ClothingItemSchema(BaseModel):
    id: str
    name: str
    image_url: str
    size: SizeEnum
