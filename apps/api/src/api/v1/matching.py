from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from src.core.security import get_current_user
from src.db.session import get_db
from src.models.user import User
from src.schemas.matching import MatchingResponse
from src.services.job_service import (
    JobNotFoundError,
    JobPermissionError,
    get_job_or_raise,
)
from src.services.matching_service import match_resume_to_job
from src.services.resume_service import get_user_resume

router = APIRouter(
    prefix="/matching",
    tags=["Matching"],
)


@router.get(
    "/jobs/{job_id}/resumes/{resume_id}",
    response_model=MatchingResponse,
)
def compare_resume_with_job(
    job_id: int,
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Compare a user's resume against a job description.
    """

    try:
        job = get_job_or_raise(
            db=db,
            user_id=current_user.id,
            job_id=job_id,
        )

        resume = get_user_resume(
            db=db,
            user=current_user,
            resume_id=resume_id,
        )

        return match_resume_to_job(
            resume=resume,
            job=job,
        )

    except JobNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except JobPermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )

    except ValueError as exc:
        message = str(exc)

        if message == "Resume not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )

        if message == "Access denied.":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=message,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )