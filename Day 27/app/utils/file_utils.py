from pathlib import Path
import shutil


# ============================================================
# DIRECTORIES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"


# ============================================================
# SUPPORTED VIDEO TYPES
# ============================================================

ALLOWED_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".webm"
}


ALLOWED_CONTENT_TYPES = {
    "video/mp4",
    "video/x-msvideo",
    "video/quicktime",
    "video/x-matroska",
    "video/webm"
}


# ============================================================
# CREATE DIRECTORIES
# ============================================================

def create_directories():

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


# ============================================================
# VALIDATE FILE
# ============================================================

def validate_video_file(filename: str, content_type: str | None):
    """
    Validate uploaded video based on extension and MIME type.
    """

    if not filename:
        raise ValueError("Missing file name.")

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported video extension: {extension}. "
            f"Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    if content_type:
        if content_type not in ALLOWED_CONTENT_TYPES:
            raise ValueError(
                f"Unsupported content type: {content_type}"
            )


# ============================================================
# SAVE UPLOAD
# ============================================================

def save_upload(upload_file, destination: Path):

    with destination.open("wb") as buffer:
        shutil.copyfileobj(
            upload_file.file,
            buffer
        )