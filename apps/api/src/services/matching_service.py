from difflib import SequenceMatcher

from src.models.job import Job
from src.models.resume import Resume
from src.schemas.matching import (
    ATSBreakdown,
    MatchingResponse,
    SkillGapResponse,
)


def _normalize_skills(skills: list | None) -> set[str]:
    """
    Normalize skills for comparison.
    """
    if not skills:
        return set()

    return {
        skill.strip().lower()
        for skill in skills
        if skill and skill.strip()
    }


def _calculate_skill_similarity(
    resume_skills: set[str],
    job_skills: set[str],
) -> tuple[int, list[str], list[str]]:
    """
    Calculate required/preferred skill match.
    """

    if not job_skills:
        return 100, [], []

    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)

    score = int((len(matched) / len(job_skills)) * 100)

    return score, missing, matched


def _calculate_keyword_score(
    resume_text: str,
    job_description: str,
) -> int:
    """
    Lightweight keyword similarity.
    """

    if not resume_text or not job_description:
        return 0

    ratio = SequenceMatcher(
        None,
        resume_text.lower(),
        job_description.lower(),
    ).ratio()

    return int(ratio * 100)


def _summary_score(summary: str) -> int:
    """
    Score resume summary quality.
    """

    if not summary:
        return 20

    length = len(summary.split())

    if length >= 60:
        return 100

    if length >= 40:
        return 90

    if length >= 25:
        return 75

    if length >= 10:
        return 60

    return 40


def _experience_score(experience: list | None) -> int:
    """
    Estimate experience completeness.
    """

    if not experience:
        return 30

    count = len(experience)

    if count >= 5:
        return 100

    if count == 4:
        return 90

    if count == 3:
        return 80

    if count == 2:
        return 70

    return 55


def _education_score(education: list | None) -> int:
    """
    Basic education completeness score.
    """

    if not education:
        return 40

    return 100


def match_resume_to_job(
    resume: Resume,
    job: Job,
) -> MatchingResponse:
    """
    Match a parsed resume against a job posting and
    generate ATS-style analysis.
    """

    parsed = resume.parsed_data or {}

    resume_skills = _normalize_skills(
        parsed.get("skills", [])
    )

    required_skills = _normalize_skills(
        job.required_skills
    )

    preferred_skills = _normalize_skills(
        job.preferred_skills
    )

    required_score, missing_skills, matched_skills = (
        _calculate_skill_similarity(
            resume_skills,
            required_skills,
        )
    )

    preferred_score, _, preferred_matches = (
        _calculate_skill_similarity(
            resume_skills,
            preferred_skills,
        )
    )

    summary = parsed.get("summary", "")

    keyword_score = _calculate_keyword_score(
        summary,
        job.description or "",
    )

    summary_score = _summary_score(summary)

    experience_score = _experience_score(
        parsed.get("experience", [])
    )

    education_score = _education_score(
        parsed.get("education", [])
    )

    overall_score = int(
        (
            required_score * 0.40
            + preferred_score * 0.10
            + keyword_score * 0.15
            + summary_score * 0.15
            + experience_score * 0.10
            + education_score * 0.10
        )
    )

    strengths = []

    if required_score >= 80:
        strengths.append(
            "Strong alignment with required skills."
        )

    if preferred_score >= 60:
        strengths.append(
            "Matches several preferred skills."
        )

    if keyword_score >= 70:
        strengths.append(
            "Resume language aligns well with the job description."
        )

    weaknesses = []

    if required_score < 60:
        weaknesses.append(
            "Missing several required technical skills."
        )

    if summary_score < 70:
        weaknesses.append(
            "Professional summary could be expanded."
        )

    if experience_score < 70:
        weaknesses.append(
            "Resume contains limited work experience."
        )

    suggestions = []

    if missing_skills:
        suggestions.append(
            f"Add or highlight these skills where applicable: {', '.join(missing_skills)}."
        )

    if summary_score < 70:
        suggestions.append(
            "Tailor the professional summary to the target role."
        )

    if keyword_score < 70:
        suggestions.append(
            "Include more keywords from the job description naturally throughout the resume."
        )

    if experience_score < 70:
        suggestions.append(
            "Add measurable achievements and project impact."
        )

    if education_score < 100:
        suggestions.append(
            "Complete the education section with all relevant qualifications."
        )

    if not suggestions:
        suggestions.append(
            "Resume is well aligned with this job posting."
        )

    return MatchingResponse(
        overall_score=overall_score,
        ats_breakdown=ATSBreakdown(
            required_skill_score=required_score,
            preferred_skill_score=preferred_score,
            keyword_score=keyword_score,
            summary_score=summary_score,
            experience_score=experience_score,
            education_score=education_score,
        ),
        skill_gap=SkillGapResponse(
            matched_skills=matched_skills,
            preferred_skill_matches=preferred_matches,
            missing_skills=missing_skills,
        ),
        strengths=strengths,
        weaknesses=weaknesses,
        suggestions=suggestions,
    )