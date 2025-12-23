from pydantic import BaseModel, HttpUrl
class LinkCreate(BaseModel):
    original_url: HttpUrl