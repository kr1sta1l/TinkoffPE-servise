from dao.product import ProductDao
from pydantic import BaseModel


class ProductDto(BaseModel):
    code: str
    title: str
    version: str
    min_principle: float
    max_principle: float
    min_term: int
    max_term: int
    min_interest: float
    max_interest: float
    min_origination: float
    max_origination: float

    @staticmethod
    def from_dao(product_dao: ProductDao) -> "ProductDto":
        return ProductDto(
            code=product_dao.code,
            title=product_dao.title,
            version=product_dao.version,
            min_principle=product_dao.min_principle,
            max_principle=product_dao.max_principle,
            min_term=product_dao.min_term,
            max_term=product_dao.max_term,
            min_interest=product_dao.min_interest,
            max_interest=product_dao.max_interest,
            min_origination=product_dao.min_origination,
            max_origination=product_dao.max_origination
        )

    def to_dao(self) -> ProductDao:
        return ProductDao(
            code=self.code,
            title=self.title,
            version=self.version,
            min_principle=self.min_principle,
            max_principle=self.max_principle,
            min_term=self.min_term,
            max_term=self.max_term,
            min_interest=self.min_interest,
            max_interest=self.max_interest,
            min_origination=self.min_origination,
            max_origination=self.max_origination
        )
