from pydantic import BaseModel, ConfigDict, Field


# Why do we need both models.py and schemas.py?
# - models.py describes how data is stored in PostgreSQL.
# - schemas.py describes what data your API accepts and returns.


# 1. The Response Schema configured to read from ORM models
class StudentCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    course: str = Field(min_length=2, max_length=50)
    year: int = Field(ge=1, le=5)


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=100)
    course: str | None = Field(default=None, min_length=2, max_length=50)
    year: int | None = Field(default=None, ge=1, le=5)


class StudentResponse(BaseModel):
    id: int
    name: str
    course: str
    year: int

# This enables Pydantic to read data from SQLAlchemy model instances
    model_config = ConfigDict(from_attributes=True) # tools for connecting FastAPI to a database using SQLAlchemy!