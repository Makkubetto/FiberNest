from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    stock: int
    unit: str = "pcs"
    description: Optional[str] = None
    image: Optional[str] = None
    badge: Optional[str] = None

class ProductUpdate(ProductCreate):
    pass

class ProductOut(BaseModel):
    id: int
    name: str
    category: str
    price: float
    stock: int
    unit: str
    description: Optional[str] = None
    image: Optional[str] = None
    badge: Optional[str] = None

    class Config:
        from_attributes = True