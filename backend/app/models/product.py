from sqlalchemy import Column, Integer, String, Float, Text
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    category    = Column(String, nullable=False)
    price       = Column(Float, nullable=False)
    stock       = Column(Integer, default=0)
    unit        = Column(String, default="pcs")
    description = Column(Text, nullable=True)
    image       = Column(String, nullable=True)
    badge       = Column(String, nullable=True)