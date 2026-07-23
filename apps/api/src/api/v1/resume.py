from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from src.core.security import get_current_user
from src.db.session import get_db
from src.models.user import User
from src.schemas.resume import (
    ResumeListResponse,
    ResumeResponse,
)
from src.services.resume_service import (
    get_user_resume,
    list_user_resumes,
    remove_resume,
    replace_resume,
    set_default_resume,
    upload_resume,
)

router = APIRouter(
    prefix="/resumes",
    tags=["Resume"],
)


@router.post(
    "/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a new resume",
)
def upload_resume_endpoint(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return upload_resume(
            db=db,
            user=current_user,
            title=title,
            file=file,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "",
    response_model=ResumeListResponse,
    summary="List all resumes",
)
def list_resumes_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resumes = list_user_resumes(
        db=db,
        user=current_user,
    )

    return ResumeListResponse(
        resumes=resumes,
    )


@router.get(
    "/{resume_id}",
    response_model=ResumeResponse,
    summary="Get a resume",
)
def get_resume_endpoint(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_user_resume(
            db=db,
            user=current_user,
            resume_id=resume_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
@router.put(
    "/{resume_id}",
    response_model=ResumeResponse,
    summary="Replace an existing resume",
)
def replace_resume_endpoint(
    resume_id: int,
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return replace_resume(
            db=db,
            user=current_user,
            resume_id=resume_id,
            title=title,
            file=file,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.patch(
    "/{resume_id}/default",
    response_model=ResumeResponse,
    summary="Set a resume as default",
)
def set_default_resume_endpoint(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return set_default_resume(
            db=db,
            user=current_user,
            resume_id=resume_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a resume",
)
def delete_resume_endpoint(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        remove_resume(
            db=db,
            user=current_user,
            resume_id=resume_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    return None