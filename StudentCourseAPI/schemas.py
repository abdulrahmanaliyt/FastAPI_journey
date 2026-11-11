from datetime import date
from pydantic import BaseModel,EmailStr, ConfigDict, Field

# --Create schemas for user registration and authentication
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


# --- Student Schemas ---
class StudentCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)


class StudentResponse(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


# --- Course Schemas ---
class CourseCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    duration: int = Field(gt=0)
    price: float | None = Field(None, ge=0)  # Optional price field


class CourseResponse(BaseModel):
    id: int
    title: str
    duration: int
    price: float | None = None
    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, ConfigDict, Field

class StudentWithCoursesResponse(BaseModel):
    id: int
    name: str
    courses: list[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
    
# --- Enrollment Schemas ---
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrollment_date: date
