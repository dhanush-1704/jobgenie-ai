from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.security import get_current_user
from src.db.session import get_db
from src.models.user import User
from src.schemas.job import (
    JobCreate,
    JobListResponse,
    JobResponse,
    JobUpdate,
)
from src.services.job_service import (
    JobNotFoundError,
    JobPermissionError,
    create_new_job,
    edit_job,
    get_job_or_raise,
    list_jobs,
    remove_job,
)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_new_job(
        db=db,
        user_id=current_user.id,
        job_data=job_data,
    )


@router.get(
    "",
    response_model=JobListResponse,
)
def get_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return JobListResponse(
        jobs=list_jobs(
            db=db,
            user_id=current_user.id,
        )
    )


@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
def get_job_by_id(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_job_or_raise(
            db=db,
            user_id=current_user.id,
            job_id=job_id,
        )
    except JobNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
    except JobPermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail=str(exc),
        )


@router.put(
    "/{job_id}",
    response_model=JobResponse,
)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return edit_job(
            db=db,
            user_id=current_user.id,
            job_id=job_id,
            job_data=job_data,
        )
    except JobNotFoundError as exc:
        raise HTTPException(404, str(exc))
    except JobPermissionError as exc:
        raise HTTPException(403, str(exc))


@router.delete(
    "/{job_id}",
    status_code=204,
)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        remove_job(
            db=db,
            user_id=current_user.id,
            job_id=job_id,
        )
    except JobNotFoundError as exc:
        raise HTTPException(404, str(exc))
    except JobPermissionError as exc:
        raise HTTPException(403, str(exc))