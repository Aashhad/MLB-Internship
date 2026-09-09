from fastapi import FastAPI

from database import Base, engine
from auth.router import router as auth_router


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# CREATE FASTAPI APP
# ============================================================

app = FastAPI(
    title="User Authentication API",
    description="FastAPI JWT Authentication System",
    version="1.0.0"
)


# ============================================================
# INCLUDE AUTH ROUTER
# ============================================================

app.include_router(auth_router)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "User Authentication API is running"
    }