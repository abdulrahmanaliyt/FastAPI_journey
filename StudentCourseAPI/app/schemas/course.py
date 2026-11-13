from pydantic import BaseModel, ConfigDict, Field


class CourseCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    duration: int = Field(gt=0)
    price: float | None = Field(default=None, ge=0)
    description: str | None = Field(default=None, max_length=500)


class CourseResponse(BaseModel):
    id: int
    title: str
    duration: int
    price: float | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)