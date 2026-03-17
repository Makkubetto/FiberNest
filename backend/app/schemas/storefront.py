from pydantic import BaseModel
from typing import List, Optional

class BannerConfig(BaseModel):
    title: str
    subtitle: str
    cta: str = "Shop Now"

class StorefrontProductItem(BaseModel):
    id: int
    name: str
    price: float
    category: str
    badge: Optional[str] = None
    image: Optional[str] = None
    emoji: Optional[str] = None

class StorefrontIn(BaseModel):
    banner: Optional[BannerConfig] = None
    new: Optional[List[StorefrontProductItem]] = []
    trending: Optional[List[StorefrontProductItem]] = []
    bestseller: Optional[List[StorefrontProductItem]] = []

class StorefrontOut(StorefrontIn):
    pass