from sqlalchemy import Column, Integer, String, DECIMAL, Double
from controllers.session import Base


class ClientDao(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    age = Column(Integer)
    phone_number = Column(String, unique=True)
    passport_id = Column(String, unique=True)
    monthly_income = Column(Double)
