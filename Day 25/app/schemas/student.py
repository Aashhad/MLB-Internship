from pydantic import BaseModel, Field, EmailStr


# Student Create Model

class StudentCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Student's full name"
    )

    age: int = Field(
        ...,
        ge=5,
        le=100,
        description="Student's age"
    )

    email: EmailStr = Field(
        ...,
        description="Student's email address"
    )

    course: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Student's course"
    )


# Student Update Model
class StudentUpdate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    age: int = Field(
        ...,
        ge=5,
        le=100
    )

    email: EmailStr

    course: str = Field(
        ...,
        min_length=2,
        max_length=100
    )


# Student Response Model

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr
    course: str

