from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class StorefrontConfig(Base):
    __tablename__ = "storefront_config"

    id    = Column(Integer, primary_key=True, index=True)
    key   = Column(String, unique=True, nullable=False)
    value = Column(Text, nullable=False)