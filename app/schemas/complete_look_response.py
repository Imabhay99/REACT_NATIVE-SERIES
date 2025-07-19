from pydantic import BaseModel

class CompleteLookResponse(BaseModel):
    recommended_items: list[str]  # or a list of another schema
