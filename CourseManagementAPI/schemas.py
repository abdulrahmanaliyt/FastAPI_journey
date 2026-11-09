from pydantic import BaseModel, ConfigDict, Field


class CourseCreate(BaseModel):
  title: str = Field(min_length=3, max_length=100)
  duration: int = Field(gt=0)
  price: float = Field(ge=0)


class CourseUpdate(BaseModel):
  title: str | None = Field(default=None, min_length=3, max_length=100)
  duration: int | None = Field(default=None, gt=0)
  price: float | None = Field(default=None, ge=0)


class CourseResponse(BaseModel):
  id: int
  title: str
  duration: int
  price: float

  model_config = ConfigDict(from_attributes=True)
#   This allows Pydantic to build response objects from SQLAlchemy model instances.