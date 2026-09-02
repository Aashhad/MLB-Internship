from fastapi import APIRouter, HTTPException, Query
from typing import List

from app.schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse
)


# CREATE ROUTER

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# IN-MEMORY DATABASE

students = [
    {
        "id": 1,
        "name": "Ashhad",
        "age": 22,
        "email": "Ashhad@gmail.com",
        "course": "Computer Science"
    },
    {
        "id": 2,
        "name": "Muhammad",
        "age": 21,
        "email": "muhammad@gmail.com",
        "course": "Artificial Intelligence"
    }
]


# GET ALL STUDENTS
# GET /students

@router.get(
    "/",
    response_model=List[StudentResponse]
)
def get_students():
    """
    Return all students.
    """

    return students


# SEARCH STUDENTS
# GET /students/search?name=ali

@router.get(
    "/search",
    response_model=List[StudentResponse]
)
def search_students(
    name: str = Query(
        ...,
        min_length=1,
        description="Search student by name"
    )
):
    """
    Search students by name.
    """

    results = [
        student
        for student in students
        if name.lower() in student["name"].lower()
    ]

    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"No student found with name '{name}'"
        )

    return results


# GET STUDENT BY ID
# GET /students/{student_id}

@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def get_student(student_id: int):
    """
    Return a specific student by ID.
    """

    for student in students:

        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail=f"Student with ID {student_id} not found"
    )


# ADD STUDENT
# POST /students

@router.post(
    "/",
    response_model=StudentResponse,
    status_code=201
)
def create_student(student: StudentCreate):
    """
    Add a new student.
    """

    # Check if email already exists
    for existing_student in students:

        if existing_student["email"] == student.email:
            raise HTTPException(
                status_code=400,
                detail="A student with this email already exists"
            )

    # Generate new ID
    if students:
        new_id = max(student["id"] for student in students) + 1
    else:
        new_id = 1

    # Create student
    new_student = {
        "id": new_id,
        "name": student.name,
        "age": student.age,
        "email": str(student.email),
        "course": student.course
    }

    # Add to in-memory list
    students.append(new_student)

    return new_student


# UPDATE STUDENT
# PUT /students/{student_id}

@router.put(
    "/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student_data: StudentUpdate
):
    """
    Update an existing student.
    """

    # Find student
    for student in students:

        if student["id"] == student_id:

            # Check duplicate email
            for existing_student in students:

                if (
                    existing_student["email"] == str(student_data.email)
                    and existing_student["id"] != student_id
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="Another student already uses this email"
                    )

            # Update student information
            student["name"] = student_data.name
            student["age"] = student_data.age
            student["email"] = str(student_data.email)
            student["course"] = student_data.course

            return student

    raise HTTPException(
        status_code=404,
        detail=f"Student with ID {student_id} not found"
    )


# DELETE STUDENT
# DELETE /students/{student_id}

@router.delete("/{student_id}")
def delete_student(student_id: int):
    """
    Delete a student by ID.
    """

    for index, student in enumerate(students):

        if student["id"] == student_id:

            deleted_student = students.pop(index)

            return {
                "message": "Student deleted successfully",
                "student": deleted_student
            }

    raise HTTPException(
        status_code=404,
        detail=f"Student with ID {student_id} not found"
    )
