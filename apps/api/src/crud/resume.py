from sqlalchemy.orm import Session

from src.models.resume import Resume


def create_resume(
    db: Session,
    resume: Resume,
) -> Resume:
    """
    Persist a new resume.
    """

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


def get_user_resumes(
    db: Session,
    user_id: int,
) -> list[Resume]:
    """
    Return all resumes belonging to a user.
    """

    return (
        db.query(Resume)
        .filter(Resume.user_id == user_id)
        .order_by(
            Resume.is_default.desc(),
            Resume.created_at.desc(),
        )
        .all()
    )


def get_resume_by_id(
    db: Session,
    resume_id: int,
) -> Resume | None:
    """
    Return a resume by its id.
    """

    return (
        db.query(Resume)
        .filter(Resume.id == resume_id)
        .first()
    )


def update_resume(
    db: Session,
    resume: Resume,
) -> Resume:
    """
    Persist changes made to a resume.
    """

    db.commit()
    db.refresh(resume)

    return resume


def update_resume_parsed_data(
    db: Session,
    resume: Resume,
    parsed_data: dict,
) -> Resume:
    """
    Store AI parsed resume data.
    """

    resume.parsed_data = parsed_data

    db.commit()
    db.refresh(resume)

    return resume


def clear_resume_parsed_data(
    db: Session,
    resume: Resume,
) -> Resume:
    """
    Remove previously parsed AI data.
    """

    resume.parsed_data = None

    db.commit()
    db.refresh(resume)

    return resume


def delete_resume(
    db: Session,
    resume: Resume,
) -> None:
    """
    Delete a resume.
    """

    db.delete(resume)
    db.commit()