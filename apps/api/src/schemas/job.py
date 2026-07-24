from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    company_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    description: str = Field(
        ...,
        min_length=1,
    )

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    employment_type: str | None = Field(
        default=None,
        max_length=100,
    )

    required_skills: list[str] | None = None

    preferred_skills: list[str] | None = None

    min_experience_years: int | None = Field(
        default=None,
        ge=0,
    )

    salary_range: str | None = Field(
        default=None,
        max_length=100,
    )


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    company_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        min_length=1,
    )

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    employment_type: str | None = Field(
        default=None,
        max_length=100,
    )

    required_skills: list[str] | None = None

    preferred_skills: list[str] | None = None

    min_experience_years: int | None = Field(
        default=None,
        ge=0,
    )

    salary_range: str | None = Field(
        default=None,
        max_length=100,
    )


class JobResponse(JobBase):
    id: int

    user_id: int

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class JobListResponse(BaseModel):
    jobs: list[JobResponse]