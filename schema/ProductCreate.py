from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(ge=0)
    stock: int = Field(ge=0)
    status: str = Field(min_length=1)
