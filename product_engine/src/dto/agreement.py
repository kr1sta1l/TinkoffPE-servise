from pydantic import BaseModel


class AgreementDto(BaseModel):
    product_code: str
    first_name: str
    second_name: str
    third_name: str
    birth_date: str
    passport_number: str
    email: str
    phone: str
    salary: float
    term: int
    interest_rate: float
    disbursment_amount: float


class AgreementStatus:
    NEW = 1
    APPROVED = 2
    REJECTED = 3
    DISBURSED = 4
    CLOSED = 5
