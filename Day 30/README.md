# Day 30 – Secure AI Processing API 

## Overview

This project extends the Day-29 FastAPI application by adding **User Authentication, JWT Security, Password Hashing, Role-Based Authorization, and User-Specific AI Processing History**.

The final architecture is:

```text
FastAPI
   ↓
Database
   ↓
Authentication
   ↓
Authorization
   ↓
Protected AI APIs
```

A logged-in user can:

- Register an account
- Login and receive a JWT access token
- View their profile
- Upload and process videos
- View their own processing jobs
- Delete their own jobs

The project also supports two roles:

1. `user`
2. `admin`

A normal user can access only their own jobs, while an admin can view processing jobs belonging to all users.

---

## Features

### Authentication

- User registration
- User login
- Password hashing using bcrypt
- JWT access tokens
- Current-user/profile endpoint
- Protected API endpoints

### Authorization

- `user` role
- `admin` role
- User ownership checks
- Admin-only endpoint
- Proper `401`, `403`, `404`, `409`, and `415` responses

### AI Processing

- Authenticated video upload
- YOLO-based video processing
- Object tracking
- Processing history stored in SQLite
- Unique object count
- Frames processed
- Processing time
- Processed video output

---

# Project Structure

```text
Day-30/
│
├── main.py
├── database.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── admin_setup.py
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── job.py
│
├── schemas/
│   ├── __init__.py
│   ├── auth.py
│   └── job.py
│
├── auth/
│   ├── __init__.py
│   ├── security.py
│   └── router.py
│
├── ai/
│   ├── __init__.py
│   ├── processor.py
│   └── router.py
│
├── model/
│   └── yolov8n.pt
│
├── uploads/
│
├── outputs/
│
└── botsort_custom.yaml
```

---

# Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT
- `python-jose`
- Passlib / bcrypt
- OpenCV
- Ultralytics YOLO
- BoT-SORT
- Uvicorn
- imageio-ffmpeg

---

# Installation

## 1. Create and activate virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

---

## 2. Install dependencies

```powershell
pip install -r requirements.txt
```

Or:

```powershell
pip install fastapi uvicorn sqlalchemy python-dotenv python-jose[cryptography] passlib[bcrypt] python-multipart email-validator opencv-python ultralytics imageio-ffmpeg
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=replace_with_your_own_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Important Security Rule

Never upload the real `.env` file to GitHub.

Add this to `.gitignore`:

```gitignore
.env
*.db
__pycache__/
*.pyc
.venv/
uploads/*
outputs/*
```

Commit only `.env.example`:

```env
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

The `SECRET_KEY` shown in `.env.example` is only a placeholder and must not be used as a production secret.

---

# Run the Application

Open the terminal inside the project directory:

```powershell
cd "C:\Users\ART\OneDrive\Desktop\ML Bench Internship\Day 30\user_authentication_codingPractice"
```

Then run:

```powershell
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Authentication

| Method | Endpoint | Authentication | Description |
|---|---|---|---|
| POST | `/auth/register` | No | Register a new user |
| POST | `/auth/login` | No | Login and receive JWT |
| GET | `/auth/me` | Yes | View current profile |

## AI Processing

| Method | Endpoint | Authentication | Description |
|---|---|---|---|
| POST | `/ai/process` | Yes | Upload/process a video |
| GET | `/ai/jobs` | Yes | View own jobs |
| GET | `/ai/jobs/{job_id}` | Yes | View own job |
| DELETE | `/ai/jobs/{job_id}` | Yes | Delete own job |
| GET | `/ai/admin/jobs` | Admin | View all users' jobs |

---

# How Registration Works

The user sends:

```http
POST /auth/register
```

Example:

```json
{
    "username": "ashhad",
    "email": "ashhad@example.com",
    "password": "MyPassword123"
}
```

The server:

1. Checks whether the username already exists.
2. Checks whether the email already exists.
3. Hashes the password.
4. Stores the hashed password in the database.
5. Assigns the default role `user`.
6. Returns the newly created user's basic information.

Example response:

```json
{
    "id": 1,
    "username": "ashhad",
    "email": "ashhad@example.com",
    "role": "user"
}
```

The password itself is never returned or stored as plain text.

---

# Password Protection

Passwords are protected using **bcrypt hashing**.

Example:

```text
Original password:

MyPassword123
```

is stored approximately as:

```text
$2b$12$.....................................................
```

The API does not store:

```text
MyPassword123
```

Instead, it verifies the entered password against the stored hash during login.

---

# How Login and JWT Authentication Work

The user sends:

```http
POST /auth/login
```

with:

```json
{
    "email": "ashhad@example.com",
    "password": "MyPassword123"
}
```

If the credentials are correct, the API returns:

```json
{
    "access_token": "JWT_TOKEN_HERE",
    "token_type": "bearer"
}
```

The client then sends the token with protected requests:

```http
Authorization: Bearer JWT_TOKEN_HERE
```

Authentication flow:

```text
Login
  ↓
Verify Email + Password
  ↓
Create JWT
  ↓
Client receives Access Token
  ↓
Client sends Bearer Token
  ↓
FastAPI validates JWT
  ↓
Current User identified
  ↓
Protected endpoint executes
```

---

# Authentication vs Authorization

## Authentication

Authentication answers:

> Who are you?

For example:

```text
Email + Password
       ↓
      Login
       ↓
   JWT Token
```

The API uses authentication to identify the current user.

## Authorization

Authorization answers:

> What are you allowed to do?

Example:

```text
User
 ↓
Can access own jobs

Admin
 ↓
Can access all jobs
```

Therefore:

```text
Authentication = Identity
Authorization = Permissions
```

---

# User Roles

The application has two roles.

## 1. User

A normal user can:

- View their profile
- Upload/process videos
- View their own jobs
- Delete their own jobs

A normal user cannot:

- View another user's jobs
- Delete another user's jobs
- Access admin endpoints

## 2. Admin

An admin can:

- View their profile
- Process videos
- View their own jobs
- Delete their own jobs
- View processing jobs of all users

---

# Creating an Admin

New registrations always receive:

```text
role = user
```

A user cannot make themselves an admin through the registration API.

To promote an existing account, run:

```powershell
python admin_setup.py
```

Enter the registered user's email.

For example:

```text
Enter user email to make admin: admin@example.com
```

The account will then have:

```text
role = admin
```

---

# Protected AI Processing

The video processing endpoint is:

```http
POST /ai/process
```

It requires a valid JWT.

Without a token:

```text
401 Unauthorized
```

With an invalid/expired token:

```text
401 Unauthorized
```

With a valid user token:

```text
201 Created
```

Processing flow:

```text
JWT Token
    ↓
Authentication
    ↓
Current User
    ↓
Upload Video
    ↓
Create Processing Job
    ↓
YOLO / Object Tracking
    ↓
Save Processed Video
    ↓
Update Database
    ↓
Return Job Information
```

---

# Processing History

Every processing job is linked to the user who created it.

Example:

```text
User 1
 ├── Job 1
 ├── Job 2
 └── Job 3

User 2
 ├── Job 4
 └── Job 5
```

When User 1 requests:

```http
GET /ai/jobs
```

the API returns only:

```text
Job 1
Job 2
Job 3
```

It does not return User 2's jobs.

---

# Job Ownership Security

For:

```http
GET /ai/jobs/{job_id}
```

and:

```http
DELETE /ai/jobs/{job_id}
```

the API checks:

```text
job.user_id == current_user.id
```

If the job belongs to another user:

```text
403 Forbidden
```

Example:

```json
{
    "detail": "You are not authorized to access this job"
}
```

This prevents users from accessing another user's processing history.

---

# Admin Access

Admins can use:

```http
GET /ai/admin/jobs
```

This endpoint is protected by the admin authorization dependency.

Normal user:

```text
403 Forbidden
```

Admin:

```text
200 OK
```

The admin can see jobs belonging to all users.

---

# HTTP Status Codes

The API uses meaningful HTTP status codes.

| Status | Meaning | Example |
|---|---|---|
| 200 | Success | Login/Profile |
| 201 | Created | Registration/Processing Job |
| 401 | Unauthorized | Missing/invalid login token |
| 403 | Forbidden | User accessing another user's job |
| 404 | Not Found | Job does not exist |
| 409 | Conflict | Email/username already exists |
| 415 | Unsupported Media Type | Unsupported video format |
| 500 | Server Error | AI processing failure |

---

# API Security Testing

The following required cases were tested.

## Test 1 – Register New User

Request:

```http
POST /auth/register
```

Expected:

```text
201 Created
```

Result:

```text
PASS
```

---

## Test 2 – Login With Correct Credentials

Request:

```http
POST /auth/login
```

Expected:

```text
200 OK
```

JWT access token returned.

Result:

```text
PASS
```

---

## Test 3 – Login With Incorrect Password

Request with an incorrect password.

Expected:

```text
401 Unauthorized
```

Error:

```json
{
    "detail": "Invalid email or password"
}
```

Result:

```text
PASS
```

---

## Test 4 – Access Protected API Without Token

Request:

```http
GET /auth/me
```

without Authorization header.

Expected:

```text
401 Unauthorized
```

Result:

```text
PASS
```

---

## Test 5 – Access API With Invalid Token

Request with an invalid JWT.

Expected:

```text
401 Unauthorized
```

Result:

```text
PASS
```

---

## Test 6 – User Accesses Another User's Job

A user attempts to access a job owned by another account.

Expected:

```text
403 Forbidden
```

Result:

```text
PASS
```

---

## Test 7 – Admin Accesses All Jobs

An authenticated admin requests:

```http
GET /ai/admin/jobs
```

Expected:

```text
200 OK
```

All users' processing jobs are returned.

Result:

```text
PASS
```

---

# Security Checklist

- [x] Passwords are hashed
- [x] Plain-text passwords are never stored
- [x] JWT authentication implemented
- [x] Protected endpoints require authentication
- [x] User ownership is checked
- [x] Admin authorization is implemented
- [x] Users cannot access other users' jobs
- [x] Users cannot make themselves admin
- [x] `.env` is excluded from Git
- [x] Database file is excluded from Git
- [x] JWT secret is stored in an environment variable
- [x] Invalid authentication returns `401`
- [x] Unauthorized resource access returns `403`

---

# GitHub Security

Before pushing the project to GitHub, make sure these files are NOT committed:

```text
.env
users.db
```

Check:

```powershell
git status
```

Your `.gitignore` should contain:

```gitignore
.env
*.db
__pycache__/
*.pyc
.venv/
uploads/*
outputs/*
```

Never commit:

- Real passwords
- JWT secret keys
- API keys
- Database credentials
- Private tokens

Use `.env.example` for configuration documentation.

---

# GitHub Commands

Initialize Git:

```powershell
git init
```

Add files:

```powershell
git add .
```

Commit:

```powershell
git commit -m "Day 30 secure AI processing API"
```

Connect your GitHub repository:

```powershell
git remote add origin https://github.com/Aashhad/MLB-Internship/tree/main
```

Push:

```powershell
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

# GitHub Repository Link

After creating the repository, add your real link here:

```text
https://github.com/Aashhad/MLB-Internship/tree/main
```

---

# Expected Outcome

The Day-30 project demonstrates a complete secure FastAPI architecture:

```text
                    ┌───────────────┐
                    │     Client    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   FastAPI     │
                    └───────┬───────┘
                            │
                  ┌─────────▼─────────┐
                  │ Authentication    │
                  │ JWT + Password    │
                  │ Hashing            │
                  └─────────┬─────────┘
                            │
                  ┌─────────▼─────────┐
                  │ Authorization      │
                  │ User / Admin       │
                  └─────────┬─────────┘
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
      ┌──────────────┐             ┌──────────────┐
      │ Protected AI │             │   Database   │
      │ Video API    │             │ Users + Jobs │
      └──────┬───────┘             └──────────────┘
             │
             ▼
      ┌──────────────┐
      │ YOLO /       │
      │ Tracking     │
      └──────┬───────┘
             │
             ▼
      Processed Video
```

## Conclusion

The Day-30 Secure AI Processing API adds a security layer to the existing FastAPI and AI application. Users authenticate with email/password, receive JWT access tokens, and use those tokens to access protected AI endpoints. Passwords are securely hashed before storage. Role-based authorization separates normal users from administrators, while job ownership checks ensure that users can access only their own processing history.

This completes the required architecture:

**FastAPI → Database → Authentication → Authorization → Protected AI APIs**
