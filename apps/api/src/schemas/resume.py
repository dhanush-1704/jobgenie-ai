from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ResumeBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )


class ResumeCreate(ResumeBase):
    pass


class ResumeUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )


class ParsedResumeResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    parsed_data: dict[str, Any] | None = None


class ResumeResponse(ResumeBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    user_id: int

    original_filename: str

    stored_filename: str

    file_path: str

    file_size: int

    mime_type: str

    is_default: bool

    parsed_data: dict[str, Any] | None = None

    created_at: datetime

    updated_at: datetime


class ResumeListResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    resumes: list[ResumeResponse]