from pathlib import Path
import os
import uuid

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from src.core.constants import (
    ALLOWED_RESUME_TYPES,
    MAX_RESUME_SIZE,
    UPLOAD_DIR,
)
from src.crud.resume import (
    create_resume,
    delete_resume,
    get_resume_by_id,
    get_user_resumes,
    update_resume,
)
from src.models.resume import Resume
from src.models.user import User
from src.services.resume_ai_service import (
    parse_resume_safe,
)


def _validate_upload(file: UploadFile) -> bytes:
    """
    Validate uploaded resume and return file bytes.
    """

    if file.content_type not in ALLOWED_RESUME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported resume format.",
        )

    contents = file.file.read()

    if len(contents) > MAX_RESUME_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume exceeds maximum allowed size.",
        )

    return contents


def _save_file(
    filename: str,
    contents: bytes,
) -> tuple[str, str]:
    """
    Save resume to disk.
    """

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    extension = Path(filename).suffix.lower()

    stored_filename = f"{uuid.uuid4()}{extension}"

    file_path = UPLOAD_DIR / stored_filename

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    return stored_filename, str(file_path)


def create_resume_record(
    db: Session,
    *,
    user: User,
    title: str,
    original_filename: str,
    stored_filename: str,
    file_path: str,
    file_size: int,
    mime_type: str,
) -> Resume:
    """
    Create a new resume metadata record.
    """

    resume = Resume(
        user_id=user.id,
        title=title,
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_path=file_path,
        file_size=file_size,
        mime_type=mime_type,
        is_default=False,
    )

    resume = create_resume(
        db,
        resume,
    )

    return parse_resume_safe(
        db=db,
        resume=resume,
    )


def upload_resume(
    db: Session,
    *,
    user: User,
    title: str,
    file: UploadFile,
) -> Resume:

    contents = _validate_upload(file)

    stored_filename, file_path = _save_file(
        file.filename,
        contents,
    )

    file.file.seek(0)

    return create_resume_record(
        db=db,
        user=user,
        title=title,
        original_filename=file.filename,
        stored_filename=stored_filename,
        file_path=file_path,
        file_size=len(contents),
        mime_type=file.content_type,
    )


def list_user_resumes(
    db: Session,
    user: User,
) -> list[Resume]:

    return get_user_resumes(
        db,
        user.id,
    )


def get_user_resume(
    db: Session,
    user: User,
    resume_id: int,
) -> Resume:

    resume = get_resume_by_id(
        db,
        resume_id,
    )

    if resume is None:
        raise ValueError(
            "Resume not found."
        )

    if resume.user_id != user.id:
        raise ValueError(
            "Access denied."
        )

    return resume


def replace_resume(
    db: Session,
    *,
    user: User,
    resume_id: int,
    file: UploadFile,
) -> Resume:

    resume = get_user_resume(
        db,
        user,
        resume_id,
    )

    contents = _validate_upload(
        file,
    )

    if os.path.exists(resume.file_path):
        os.remove(
            resume.file_path,
        )

    stored_filename, file_path = _save_file(
        file.filename,
        contents,
    )

    file.file.seek(0)

    resume.original_filename = file.filename
    resume.stored_filename = stored_filename
    resume.file_path = file_path
    resume.file_size = len(contents)
    resume.mime_type = file.content_type

    resume = update_resume(
        db,
        resume,
    )

    return parse_resume_safe(
        db=db,
        resume=resume,
    )


def remove_resume(
    db: Session,
    user: User,
    resume_id: int,
) -> None:

    resume = get_user_resume(
        db,
        user,
        resume_id,
    )

    delete_resume(
        db,
        resume,
    )

    if os.path.exists(
        resume.file_path,
    ):
        os.remove(
            resume.file_path,
        )


def set_default_resume(
    db: Session,
    user: User,
    resume_id: int,
) -> Resume:

    resumes = get_user_resumes(
        db,
        user.id,
    )

    selected = None

    for resume in resumes:
        resume.is_default = (
            resume.id == resume_id
        )

        update_resume(
            db,
            resume,
        )

        if resume.is_default:
            selected = resume

    if selected is None:
        raise ValueError(
            "Resume not found."
        )

    return selected