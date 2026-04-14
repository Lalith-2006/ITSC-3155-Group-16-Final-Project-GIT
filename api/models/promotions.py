from sqlalchemy import Column, Integer, String
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True)
    discount = Column(Integer)
    expiration_date = Column(String(50))