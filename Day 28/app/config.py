from pathlib import Path


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# DIRECTORIES
# ============================================================

MODEL_DIR = BASE_DIR / "models"

INPUT_DIR = BASE_DIR / "videos" / "input"

OUTPUT_DIR = BASE_DIR / "videos" / "output"

LOG_DIR = BASE_DIR / "logs"


# Create directories automatically
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# MODEL
# ============================================================

MODEL_PATH = MODEL_DIR / "yolov8n.pt"


# ============================================================
# VIDEO VALIDATION
# ============================================================

# Maximum video size = 100 MB
MAX_VIDEO_SIZE = 100 * 1024 * 1024


# Supported extensions
ALLOWED_VIDEO_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".webm",
}


# Supported MIME types
ALLOWED_VIDEO_CONTENT_TYPES = {
    "video/mp4",
    "video/x-msvideo",
    "video/quicktime",
    "video/x-matroska",
    "video/webm",
}


# ============================================================
# CONFIDENCE
# ============================================================

MIN_CONFIDENCE = 0.0
MAX_CONFIDENCE = 1.0

DEFAULT_CONFIDENCE = 0.25