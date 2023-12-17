import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import ValidationError
from starlette.responses import JSONResponse

from controllers.session import repository

from dao.product import ProductDao
from dto.product import ProductDto
from dao.agreement import AgreementDao
from dto.agreement import AgreementDto, AgreementStatus
from dao.client import ClientDao

from fastapi.exceptions import RequestValidationError

from functions.agreement_creation import birthdate_to_age, convert_phone_number, \
    update_client, get_origination_amount, check_email
from datetime import datetime

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": "Некорректный формат данных"})


@app.exception_handler(400)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"message": exc.detail})


@app.get("/product")
async def get_products() -> list[ProductDto]:
    products = await repository.get_all(ProductDao)
    return [ProductDto.from_dao(product) for product in products]


@app.get("/product/{product_code}", responses={404: {"description": "Product not found"},
                                               200: {"description": "Product found"}})
async def get_product_by_code(product_code: str):
    product = await repository.get_one_by_expression(ProductDao, ProductDao.code == product_code)
    if not product:
        return Response(status_code=404)
    return ProductDto.from_dao(product)


@app.post("/product", responses={400: {"description": "Invalid product data"},
                                 409: {"description": "Product already exists",
                                       200: {"description": "Product created"}}})
async def create_product(product: ProductDto):
    db_product = await repository.get_one_by_expression(ProductDao, ProductDao.code == product.code)
    db_title_version = await repository.get_one_by_expression(ProductDao, (ProductDao.title == product.title) and (
            ProductDao.version == product.version))
    if db_product or db_title_version:
        return Response(status_code=409)

    product_dao = product.to_dao()
    await repository.save(product_dao)
    return Response(status_code=200)


@app.delete("/product/{product_code}", responses={404: {"description": "Product not found"},
                                                  200: {"description": "Product deleted"}})
async def delete_product(product_code: str):
    product = (await repository.get_one_by_expression(ProductDao, ProductDao.code == product_code))
    if not product:
        return Response(status_code=404)
    await repository.delete(product)
    return Response(status_code=200)


@app.post("/agreement", responses={400: {"description": "Invalid agreement data"},
                                   409: {"description": "Agreement already exists",
                                         200: {"description": "Agreement created"}}})
async def create_agreement(agreement_dto: AgreementDto):
    product = (await repository.get_one_by_expression(ProductDao, ProductDao.code == agreement_dto.product_code))
    if not product:
        raise HTTPException(status_code=400, detail="Продукта с таким кодом не существует")

    try:
        birth_date = datetime.strptime(agreement_dto.birth_date, "%Y.%m.%d").date()
        client_age: int = birthdate_to_age(birth_date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        phone_number: str = convert_phone_number(agreement_dto.phone)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # хз, ранее обсуждалось, что почту хранить не будем, но валидацию оставил - мало ли что потом поменяется
    if not check_email(agreement_dto.email):
        raise HTTPException(status_code=400, detail="Некорректный формат email")

    logging.warning(f"{product.min_principle} | {agreement_dto.disbursment_amount} | {product.max_principle}")
    if agreement_dto.disbursment_amount < product.min_principle or \
            agreement_dto.disbursment_amount > product.max_principle:
        raise HTTPException(status_code=400, detail="Некорректная сумма выдачи")

    logging.warning(f"{product.min_term} | {agreement_dto.term} | {product.max_term}")
    if agreement_dto.term < product.min_term or \
            agreement_dto.term > product.max_term:
        raise HTTPException(status_code=400, detail="Некорректный срок выдачи")

    # проверить на существование клиента
    client: ClientDao or None = await repository.get_one_by_expression(ClientDao,
                                                                       ClientDao.passport_id == agreement_dto.passport_number)
    if not client:
        # Создать клиента
        try:
            client = ClientDao(surname=agreement_dto.first_name,
                               name=agreement_dto.second_name,
                               patronymic=agreement_dto.third_name,
                               age=client_age,
                               phone_number=phone_number,
                               passport_id=agreement_dto.passport_number,
                               monthly_income=agreement_dto.salary)
            await repository.save(client)
        except ValueError:
            raise HTTPException(status_code=400, detail="Некорректный формат данных")
    else:
        # Обновить данные клиента или вернуть ошибку, если различие в неизменяемых полях
        try:
            client = await update_client(agreement_dto, client_age, phone_number, client)
            await repository.save(client)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    try:
        agreement = AgreementDao(product_code=agreement_dto.product_code,
                                 client_id=client.id,
                                 create_datetime=datetime.now(),
                                 status=AgreementStatus.NEW,
                                 principle_amount=agreement_dto.disbursment_amount,
                                 term=agreement_dto.term,
                                 origination_amount=await get_origination_amount(product),
                                 interest_rate=agreement_dto.interest_rate,
                                 disbursement_datetime=None)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Некорректный формат данных")
    await repository.save(agreement)
    return JSONResponse(status_code=200, content={"agreement_id": agreement.id})
