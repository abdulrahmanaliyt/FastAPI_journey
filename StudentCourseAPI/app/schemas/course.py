
from pydantic import BaseModel, ConfigDict, Field, model_validator


class CourseCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    duration: int = Field(gt=0)
    price: float | None = Field(default=None, ge=0)
    description: str | None = Field(default=None, max_length=500)


class CourseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    duration: int | None = Field(default=None, gt=0)
    price: float | None = Field(default=None, ge=0)
    description: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def validate_required_fields(self):
        if "title" in self.model_fields_set and self.title is None:
            raise ValueError("title cannot be null")

        if "duration" in self.model_fields_set and self.duration is None:
            raise ValueError("duration cannot be null")

        return self


class CourseResponse(BaseModel):
    id: int
    title: str
    duration: int
    price: float | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)

class CourseReplace(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    duration: int = Field(gt=0)
    price: float | None = Field(default=None, ge=0)
    description: str | None = Field(default=None, max_length=500)