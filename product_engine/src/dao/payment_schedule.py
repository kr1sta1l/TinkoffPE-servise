from sqlalchemy import Column, Integer, DateTime
from controllers.session import Base


class PaymentScheduleDao(Base):
    __tablename__ = "payment_schedule"

    agreement_id = Column(Integer, primary_key=True, index=True)
    planned_payment_date = Column(DateTime(timezone=True))
    real_payment_date = Column(DateTime(timezone=True))
    principle_payment = Column(Integer)
    interest_payment = Column(Integer)
    status = Column(Integer)
    payment_number = Column(Integer)
    paid_sum = Column(Integer)
