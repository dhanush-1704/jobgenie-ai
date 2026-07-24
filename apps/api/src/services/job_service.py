from sqlalchemy.orm import Session

from src.crud.job import (
    create_job,
    delete_job,
    get_job_by_id,
    get_user_jobs,
    update_job,
)
from src.models.job import Job
from src.schemas.job import JobCreate, JobUpdate


class JobNotFoundError(Exception):
    """Raised when a job cannot be found."""
    pass


class JobPermissionError(Exception):
    """Raised when a user attempts to access another user's job."""
    pass


def create_new_job(
    db: Session,
    user_id: int,
    job_data: JobCreate,
) -> Job:
    """
    Create a new job.
    """

    job = Job(
        user_id=user_id,
        **job_data.model_dump(),
    )

    return create_job(
        db=db,
        job=job,
    )


def list_jobs(
    db: Session,
    user_id: int,
) -> list[Job]:
    """
    Return all jobs belonging to a user.
    """

    return get_user_jobs(
        db=db,
        user_id=user_id,
    )


def get_job(
    db: Session,
    job_id: int,
) -> Job | None:
    """
    Return a job by its ID or None if it does not exist.
    """

    return get_job_by_id(
        db=db,
        job_id=job_id,
    )


def get_job_or_raise(
    db: Session,
    user_id: int,
    job_id: int,
) -> Job:
    """
    Return a job after validating ownership.
    """

    job = get_job(
        db=db,
        job_id=job_id,
    )

    if job is None:
        raise JobNotFoundError("Job not found.")

    if job.user_id != user_id:
        raise JobPermissionError(
            "You do not have permission to access this job."
        )

    return job


def edit_job(
    db: Session,
    user_id: int,
    job_id: int,
    job_data: JobUpdate,
) -> Job:
    """
    Update an existing job.
    """

    job = get_job_or_raise(
        db=db,
        user_id=user_id,
        job_id=job_id,
    )

    updates = job_data.model_dump(
        exclude_unset=True,
    )

    for field, value in updates.items():
        setattr(job, field, value)

    return update_job(
        db=db,
        job=job,
    )


def remove_job(
    db: Session,
    user_id: int,
    job_id: int,
) -> None:
    """
    Delete a job.
    """

    job = get_job_or_raise(
        db=db,
        user_id=user_id,
        job_id=job_id,
    )

    delete_job(
        db=db,
        job=job,
    )