from sqlalchemy import Column, Integer, String, DECIMAL, Double, TIMESTAMP
from controllers.session import Base


class PaymentScheduleDao(Base):
    __tablename__ = "payment_schedule"

    agreement_id = Column(Integer, primary_key=True, index=True)
    planned_payment_date = Column(TIMESTAMP)
    real_payment_date = Column(TIMESTAMP)
    principle_payment = Column(Integer)
    interest_payment = Column(Integer)
    status = Column(Integer)
    payment_number = Column(Integer)
    paid_sum = Column(Integer)
