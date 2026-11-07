from pydantic import BaseModel, ConfigDict, Field


class ProductUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1)
    price: float | None = Field(default=None, ge=0)
    stock: int | None = Field(default=None, ge=0)
    status: str | None = Field(default=None, min_length=1)
