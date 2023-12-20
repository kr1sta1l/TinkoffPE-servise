import random

from dao.client import ClientDao
from dao.product import ProductDao
from dto.agreement import AgreementDto
import datetime
import re


def birthdate_to_age(birthdate: datetime.date) -> int:
    today = datetime.date.today()
    age = today.year - birthdate.year
    if today.month < birthdate.month or (today.month == birthdate.month and today.day < birthdate.day):
        age -= 1

    if age < 0:
        raise ValueError('Некорректная дата рождения')
    return age


def check_phone_number(phone_number: str) -> bool:
    result = re.match(r'^(\+?)(\d{1,3})?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
                      phone_number)
    return bool(result)


def check_email(email: str) -> bool:
    result = re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email)
    return bool(result)


def convert_phone_number(phone_number: str) -> str:
    phone_number = str(phone_number)
    if check_phone_number(phone_number):
        return re.sub(r'\D', '', phone_number)
    else:
        raise ValueError('Некорректный формат номера телефона')


async def update_client(agreement_dto: AgreementDto, client_age: int, phone_number: str,
                        client: ClientDao) -> ClientDao | tuple:
    # Проверка на фио клиента
    if client.surname != agreement_dto.first_name or \
            client.name != agreement_dto.second_name or \
            client.patronymic != agreement_dto.third_name:
        raise ValueError("Некорректные ФИО клиента")

    if client_age < 18:
        raise ValueError("Клиент несовершеннолетний")

    if (client.monthly_income != agreement_dto.salary or client.phone_number != phone_number or
            client.age != client_age):
        # Обновить данные клиента
        client.monthly_income = agreement_dto.salary
        client.phone_number = phone_number
        client.age = client_age
    return client


async def get_origination_amount(product: ProductDao) -> float:
    return float(random.uniform(float(product.min_principle), float(product.max_principle)))
