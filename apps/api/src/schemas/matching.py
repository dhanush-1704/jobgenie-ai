from pydantic import BaseModel, ConfigDict, Field


class ATSBreakdown(BaseModel):
    required_skill_score: int = Field(..., ge=0, le=100)
    preferred_skill_score: int = Field(..., ge=0, le=100)
    keyword_score: int = Field(..., ge=0, le=100)
    summary_score: int = Field(..., ge=0, le=100)
    experience_score: int = Field(..., ge=0, le=100)
    education_score: int = Field(..., ge=0, le=100)


class SkillGapResponse(BaseModel):
    matched_skills: list[str]
    preferred_skill_matches: list[str]
    missing_skills: list[str]


class MatchingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    overall_score: int = Field(..., ge=0, le=100)

    ats_breakdown: ATSBreakdown

    skill_gap: SkillGapResponse

    strengths: list[str]

    weaknesses: list[str]

    suggestions: list[str]