from pydantic import BaseModel, Field


class ATSBreakdown(BaseModel):
    required_skill_score: int = Field(..., ge=0, le=100)
    preferred_skill_score: int = Field(..., ge=0, le=100)
    keyword_score: int = Field(..., ge=0, le=100)
    summary_score: int = Field(..., ge=0, le=100)
    experience_score: int = Field(..., ge=0, le=100)
    education_score: int = Field(..., ge=0, le=100)


class ATSSuggestion(BaseModel):
    category: str
    message: str


class ATSResponse(BaseModel):
    ats_score: int = Field(..., ge=0, le=100)

    breakdown: ATSBreakdown

    strengths: list[str]

    weaknesses: list[str]

    suggestions: list[ATSSuggestion]