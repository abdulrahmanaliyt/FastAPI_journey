from datetime import date

from pydantic import BaseModel, ConfigDict


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrollment_date: date

    model_config = ConfigDict(from_attributes=True)