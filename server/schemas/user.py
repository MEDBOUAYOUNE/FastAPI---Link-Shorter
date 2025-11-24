from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    full_name: Optional[str] = None
    email: EmailStr
    password: str