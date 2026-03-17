from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class OrderItemIn(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    items: List[OrderItemIn]
    payment_method: str
    delivery_method: str
    delivery_address: Optional[str] = None
    notes: Optional[str] = None
    subtotal: float
    shipping_fee: float = 0
    total: float

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    name: Optional[str] = None

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    user_id: int
    status: str
    payment_method: str
    delivery_method: str
    delivery_address: Optional[str] = None
    notes: Optional[str] = None
    subtotal: float
    shipping_fee: float
    total: float
    created_at: datetime
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str