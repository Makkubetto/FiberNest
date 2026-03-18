from sqlalchemy import Column, Integer, String, Enum, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id        = Column(Integer, primary_key=True, index=True)
    email     = Column(String, unique=True, index=True, nullable=False)
    password  = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    address   = Column(String, nullable=True)
    mobile    = Column(String, nullable=True)
    role      = Column(Enum("buyer", "seller", name="user_role"), default="buyer", nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)