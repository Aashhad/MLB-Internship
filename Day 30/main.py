from fastapi import FastAPI

from database import Base, engine

# Import models BEFORE create_all
from models.user import User
from models.job import ProcessingJob

from auth.router import router as auth_router

from ai.router import router as ai_router


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

Base.metadata.create_all(
    bind=engine
)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(

    title="Secure AI Processing API",

    description=(
        "JWT Authentication + "
        "Role-Based Authorization + "
        "AI Video Processing"
    ),

    version="1.0.0"
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(
    auth_router
)

app.include_router(
    ai_router
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "Secure AI Processing API is running"
    }