from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id               = Column(Integer, primary_key=True, index=True)
    user_id          = Column(Integer, ForeignKey("users.id"), nullable=False)
    status           = Column(String, default="Pending")
    payment_method   = Column(String, nullable=False)
    delivery_method  = Column(String, nullable=False)
    delivery_address = Column(Text, nullable=True)
    notes            = Column(Text, nullable=True)
    subtotal         = Column(Float, nullable=False)
    shipping_fee     = Column(Float, default=0)
    total            = Column(Float, nullable=False)
    created_at       = Column(DateTime, default=datetime.utcnow)

    user  = relationship("User")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id         = Column(Integer, primary_key=True, index=True)
    order_id   = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity   = Column(Integer, nullable=False)
    price      = Column(Float, nullable=False)

    order   = relationship("Order", back_populates="items")
    product = relationship("Product")