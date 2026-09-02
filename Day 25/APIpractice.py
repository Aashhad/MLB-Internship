from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


# CREATE FASTAPI APPLICATION

app = FastAPI(
    title="Student Management API",
    description="A simple FastAPI application for managing students",
    version="1.0.0"
)

# PYDANTIC MODEL

class Student(BaseModel):
    name: str = Field(
        min_length=2,
        description="Student's full name"
    )

    age: int = Field(
        gt=0,
        description="Student's age"
    )

    course: str = Field(
        min_length=2,
        description="Student's course"
    )


# TEMPORARY IN-MEMORY DATABASE

students = [
    {
        "id": 1,
        "name": "Ashhad",
        "age": 23,
        "course": "Computer Science"
    },
    {
        "id": 2,
        "name": "Muhammad",
        "age": 22,
        "course": "Artificial Intelligence"
    }
]


# GET /
# Welcome endpoint

@app.get("/")
def home():
    return {
        "message": "Welcome to Student Management API"
    }


# GET /health
# Health check endpoint

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# GET /students
# Get all students

@app.get("/students")
def get_students():
    return students


# POST /students
# Add a new student

@app.post("/students")
def create_student(student: Student):

    new_student = {
        "id": len(students) + 1,
        **student.model_dump()
    }

    students.append(new_student)

    return new_student


# GET /students/{student_id}
# Get a specific student

@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:

        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )
