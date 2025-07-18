from pydantic import BaseModel

class CompleteLookResponse(BaseModel):
    outfit_items: list[str]  # or a list of another schema
