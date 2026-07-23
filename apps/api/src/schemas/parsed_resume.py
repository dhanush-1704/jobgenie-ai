from pydantic import BaseModel


class Education(BaseModel):
    degree: str
    institution: str
    year: str


class Experience(BaseModel):
    company: str
    designation: str
    duration: str
    description: str


class Project(BaseModel):
    title: str
    description: str
    technologies: list[str]


class ParsedResume(BaseModel):
    name: str
    email: str
    phone: str
    summary: str

    skills: list[str]

    education: list[Education]

    experience: list[Experience]

    projects: list[Project]

    certifications: list[str]

    languages: list[str]