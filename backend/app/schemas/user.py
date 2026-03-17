from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    address: Optional[str] = None
    mobile: Optional[str] = None
    role: str = "buyer"

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    address: Optional[str] = None
    mobile: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    address: Optional[str] = None
    mobile: Optional[str] = None
    role: str

    class Config:
        from_attributes = True

class ChangePassword(BaseModel):
    current_password: str
    new_password: str