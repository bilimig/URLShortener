from pydantic import BaseModel

class URLCreate(BaseModel):
    original_url: str

class URLResponse(BaseModel):
    original_url: str
    short_url: str

    class Config:
        from_attributes = True