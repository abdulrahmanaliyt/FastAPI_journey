# schemas.py
from pydantic import BaseModel, Field, EmailStr

# Request model
class StudentCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(ge=16, le=60)
    course: str = Field(min_length=2, max_length=20)

# Response model
class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    course: str

# Temporary database
students = []