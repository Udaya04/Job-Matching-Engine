from typing import List, Optional, Tuple
from pydantic import BaseModel, Field

class Education(BaseModel):
    degree: str
    field: str
    cgpa: float = Field(..., ge=0, le=10)

class Candidate(BaseModel):
    skills: List[str]
    experience_years: int = Field(..., ge=0)
    preferred_locations: List[str]
    preferred_roles: List[str]
    expected_salary: int
    education: Education

class Job(BaseModel):
    job_id: str
    title: str
    required_skills: List[str]
    experience_required: str  # e.g. "0-2 years"
    location: str
    salary_range: Tuple[int, int]
    company: str

class MatchRequest(BaseModel):
    candidate: Candidate
    jobs: List[Job]

class MatchBreakdown(BaseModel):
    skill_match: float
    location_match: float
    salary_match: float
    experience_match: float
    role_match: float

class MatchResponse(BaseModel):
    job_id: str
    match_score: float
    breakdown: MatchBreakdown
    missing_skills: List[str]
    recommendation_reason: str
