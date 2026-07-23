from sqlalchemy.orm import Session

from src.ai.extractor import ResumeExtractor
from src.ai.parser import ResumeParser
from src.crud.resume import (
    clear_resume_parsed_data,
    update_resume_parsed_data,
)
from src.models.resume import Resume


def parse_resume(
    db: Session,
    resume: Resume,
) -> Resume:
    """
    Extract text from a resume, parse it using the AI model,
    and persist the structured output.
    """

    extracted_text = ResumeExtractor.extract(
        resume.file_path,
    )

    if not extracted_text:
        raise ValueError(
            "Unable to extract text from resume."
        )

    extracted_text = extracted_text.strip()

    if not extracted_text:
        raise ValueError(
            "Resume contains no readable text."
        )

    parsed_data = ResumeParser.parse(
        extracted_text,
    )

    return update_resume_parsed_data(
        db=db,
        resume=resume,
        parsed_data=parsed_data,
    )


def reparse_resume(
    db: Session,
    resume: Resume,
) -> Resume:
    """
    Clear previously parsed data and run the parser again.
    """

    clear_resume_parsed_data(
        db=db,
        resume=resume,
    )

    return parse_resume(
        db=db,
        resume=resume,
    )


def parse_resume_safe(
    db: Session,
    resume: Resume,
) -> Resume:
    """
    Parse a resume without interrupting the upload flow.

    If parsing fails, the resume remains uploaded and
    parsed_data stays None.
    """

    try:
        return parse_resume(
            db=db,
            resume=resume,
        )
    except Exception:
        return resume