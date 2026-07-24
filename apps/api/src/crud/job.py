from sqlalchemy.orm import Session

from src.models.job import Job


def create_job(
    db: Session,
    job: Job,
) -> Job:
    """
    Persist a new job.
    """

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_user_jobs(
    db: Session,
    user_id: int,
) -> list[Job]:
    """
    Return all jobs belonging to a user.
    """

    return (
        db.query(Job)
        .filter(Job.user_id == user_id)
        .order_by(
            Job.created_at.desc(),
        )
        .all()
    )


def get_job_by_id(
    db: Session,
    job_id: int,
) -> Job | None:
    """
    Return a job by its id.
    """

    return (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )


def update_job(
    db: Session,
    job: Job,
) -> Job:
    """
    Persist changes made to a job.
    """

    db.commit()
    db.refresh(job)

    return job


def delete_job(
    db: Session,
    job: Job,
) -> None:
    """
    Delete a job.
    """

    db.delete(job)
    db.commit()