from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.types import DateTime

from controllers.session import Base


class AgreementDao(Base):
    __tablename__ = "agreement"

    id = Column(Integer, primary_key=True, index=True)
    product_code = Column(String, index=True)
    client_id = Column(Integer, index=True)
    create_datetime = Column(DateTime(timezone=True))
    status = Column(Integer)
    principle_amount = Column(Integer)
    term = Column(Integer)
    origination_amount = Column(Integer)
    interest_rate = Column(DECIMAL)
    disbursement_datetime = Column(DateTime(timezone=True))
