from fastapi import FastAPI

from app.routes.video import router as video_router


# ============================================================
# CREATE APPLICATION
# ============================================================

app = FastAPI(
    title="AI Video Processing API",
    description=(
        "FastAPI + YOLO API for background video processing."
    ),
    version="1.0.0"
)


# ============================================================
# REGISTER ROUTER
# ============================================================

app.include_router(
    video_router
)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
async def root():

    return {
        "message": "AI Video Processing API is running.",
        "docs": "/docs"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }