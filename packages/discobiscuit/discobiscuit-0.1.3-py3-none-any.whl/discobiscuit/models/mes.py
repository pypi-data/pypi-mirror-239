from pydantic import BaseModel


class Product(BaseModel):
    itemcode: str
    version: str
    revision: str
