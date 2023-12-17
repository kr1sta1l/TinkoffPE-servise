from sqlalchemy import Column, Integer, String, DECIMAL, Double
from controllers.session import Base


class ProductDao(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    title = Column(String)
    version = Column(String)
    min_principle = Column(DECIMAL)
    max_principle = Column(DECIMAL)
    min_term = Column(Integer)
    max_term = Column(Integer)
    min_interest = Column(DECIMAL)
    max_interest = Column(DECIMAL)
    min_origination = Column(Double)
    max_origination = Column(Double)
