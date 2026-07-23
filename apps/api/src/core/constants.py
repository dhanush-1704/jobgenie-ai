from pathlib import Path

UPLOAD_DIR = Path("uploads/resumes")

ALLOWED_RESUME_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

MAX_RESUME_SIZE = 5 * 1024 * 1024  # 5 MB