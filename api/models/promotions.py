from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String(50), unique=True, index=True)

    discount = Column(Integer)

    expiration_date = Column(DateTime)

    is_active = Column(Boolean, default=True)