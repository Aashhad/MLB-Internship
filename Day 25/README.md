# FastAPI REST API

A simple REST API built with **FastAPI** and **Pydantic**. This project demonstrates the basics of creating API endpoints, handling HTTP requests, validating data, and returning JSON responses.

---

## 📌 What is a REST API?

**REST** stands for **Representational State Transfer**. A REST API is a way for different applications or systems to communicate with each other over HTTP.

A REST API uses standard HTTP methods such as:

* **GET** → Retrieve data
* **POST** → Create new data
* **PUT** → Update existing data
* **DELETE** → Delete data

For example, a student management API might provide:

```text
GET    /students       → Get all students
GET    /students/{id}  → Get a specific student
POST   /students       → Create a new student
PUT    /students/{id}  → Update a student
DELETE /students/{id}  → Delete a student
```

REST APIs commonly exchange data using **JSON (JavaScript Object Notation)**.

---

## 🔄 Difference Between GET and POST

### GET

The **GET** method is used to retrieve data from the server.

Example:

```http
GET /students
```

Response:

```json
[
    {
        "id": 1,
        "name": "Ashhad",
        "age": 21,
        "email": "ashhad@example.com"
    },
    {
        "id": 2,
        "name": "Muhammad",
        "age": 22,
        "email": "muhammad@example.com"
    }
]
```

GET requests normally do not contain a request body. Data can be passed through URL parameters or query parameters.

Example:

```http
GET /students/1
```

---

### POST

The **POST** method is used to send data to the server, usually to create a new resource.

Example:

```http
POST /students
```

Request body:

```json
{
    "name": "Hamza",
    "age": 20,
    "email": "hamza@example.com"
}
```

Response:

```json
{
    "id": 3,
    "name": "Hamza",
    "age": 20,
    "email": "hamza@example.com"
}
```

### GET vs POST

| Feature             | GET                  | POST             |
| ------------------- | -------------------- | ---------------- |
| Purpose             | Retrieve data        | Create/send data |
| Request Body        | Usually not used     | Commonly used    |
| Changes Server Data | No                   | Usually yes      |
| Example             | `GET /students`      | `POST /students` |
| Data Location       | URL/query parameters | Request body     |

---

## 🐍 What is Pydantic Used For?

**Pydantic** is a Python library used for **data validation and data parsing**.

FastAPI uses Pydantic models to define the structure of request and response data.

For example:

```python
from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    age: int
    email: str
```

This model requires:

* `name` to be a string
* `age` to be an integer
* `email` to be a string

If the client sends invalid data, FastAPI automatically validates the request and returns an appropriate validation error.

Example invalid request:

```json
{
    "name": "Ashhad",
    "age": "twenty",
    "email": "ashhad@example.com"
}
```

The `age` field is expected to be an integer, so Pydantic will detect the invalid input.

### Benefits of Pydantic

* Validates incoming data
* Defines clear data structures
* Provides type checking
* Helps prevent invalid input
* Automatically generates API schemas
* Works directly with FastAPI
* Makes request and response models easier to maintain

---

## 🏗️ API Structure

The project follows a modular structure so that routes, schemas, and application configuration are separated.

```text
project/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── routes/
│   │   └── students.py
│   │
│   └── schemas/
│       └── student.py
│
├── requirements.txt
└── README.md
```

### `app/main.py`

This is the main entry point of the FastAPI application.

It creates the FastAPI application and includes the API routers.

Example:

```python
from fastapi import FastAPI
from app.routes.students import router as student_router

app = FastAPI(
    title="Student REST API",
    description="A simple REST API built with FastAPI",
    version="1.0.0"
)

app.include_router(student_router)
```

---

### `app/routes/students.py`

This file contains the student-related API endpoints.

Example:

```python
from fastapi import APIRouter

from app.schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse
)

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)
```

The router keeps student endpoints organized separately from the main application.

---

### `app/schemas/student.py`

This file contains Pydantic models used for validating request and response data.

Example:

```python
from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    age: int
    email: str


class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    email: str | None = None


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    email: str
```

---

## 🚀 Running the API

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

---

## 📚 API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows you to:

* View available endpoints
* Test API requests
* Enter request data
* View API responses
* Check validation errors

### ReDoc

FastAPI also provides ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# 🔗 API Endpoints

## 1. Welcome Endpoint

### Request

```http
GET /
```

### Response

```json
{
    "message": "Welcome to the FastAPI REST API"
}
```

---

## 2. Health Check

### Request

```http
GET /health
```

### Response

```json
{
    "status": "healthy"
}
```

This endpoint can be used to check whether the API is running correctly.

---

# 👨‍🎓 Student API Examples

## 3. Get All Students

### Request

```http
GET /students
```

### Response

```json
[
    {
        "id": 1,
        "name": "Ashhad",
        "age": 21,
        "email": "ashhad@example.com"
    },
    {
        "id": 2,
        "name": "Muhammad",
        "age": 22,
        "email": "muhammad@example.com"
    }
]
```

---

## 4. Get a Student by ID

### Request

```http
GET /students/1
```

### Response

```json
{
    "id": 1,
    "name": "Ashhad",
    "age": 21,
    "email": "ashhad@example.com"
}
```

If the student does not exist, the API can return an error such as:

```json
{
    "detail": "Student not found"
}
```

---

## 5. Create a Student

### Request

```http
POST /students
```

### Request Body

```json
{
    "name": "Hamza",
    "age": 20,
    "email": "hamza@example.com"
}
```

### Response

```json
{
    "id": 3,
    "name": "Hamza",
    "age": 20,
    "email": "hamza@example.com"
}
```

---

## 6. Update a Student

### Request

```http
PUT /students/3
```

### Request Body

```json
{
    "name": "Muhammad Ashhad",
    "age": 21,
    "email": "ashhad03@example.com"
}
```

### Response

```json
{
    "id": 3,
    "name": "Muhammad Ashhad",
    "age": 21,
    "email": "ashhad03@example.com"
}
```

---

## 7. Delete a Student

### Request

```http
DELETE /students/3
```

### Response

```json
{
    "message": "Student deleted successfully"
}
```

---

# 🧪 Testing with Swagger

After starting the server, open:

```text
http://127.0.0.1:8000/docs
```

Select an endpoint such as:

```text
POST /students
```

Click **Try it out**, enter the JSON request body, and click **Execute**.

FastAPI will display the request, response status code, and response JSON.

---

# 📦 Technologies Used

* **Python** — Programming language
* **FastAPI** — Web framework for building APIs
* **Pydantic** — Data validation and schema definitions
* **Uvicorn** — ASGI server
* **JSON** — Data exchange format
* **Swagger/OpenAPI** — API documentation

---

# 🎯 Learning Objectives

This project demonstrates the fundamentals of backend API development:

* Understanding APIs
* Understanding REST architecture
* Working with HTTP methods
* Creating FastAPI endpoints
* Handling GET and POST requests
* Using Pydantic models
* Validating request data
* Returning JSON responses
* Organizing a FastAPI project
* Testing APIs with Swagger UI
* Understanding automatic OpenAPI documentation

---

# 📌 Conclusion

This project provides a basic introduction to building REST APIs with FastAPI. FastAPI makes it easy to create high-performance APIs while Pydantic provides powerful data validation and type-based schemas.

The modular structure also makes the application easier to maintain and expand as more features and endpoints are added.

## 👨‍💻 Author

**Muhammad Ashhad**