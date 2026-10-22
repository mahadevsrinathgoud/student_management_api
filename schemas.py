
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(ge=16, le=100)
    course: str = Field(min_length=2, max_length=100)
    marks: float = Field(ge=0, le=100)


class StudentResponse(StudentCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
