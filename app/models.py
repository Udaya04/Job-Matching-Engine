from enum import Enum
from dataclasses import dataclass
from typing import Dict, List


# ----------------------------
# Enums
# ----------------------------

class MatchFactor(str, Enum):
    SKILL = "skill"
    LOCATION = "location"
    SALARY = "salary"
    EXPERIENCE = "experience"
    ROLE = "role"


class ExperienceLevel(str, Enum):
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"


# ----------------------------
# Scoring Weights
# ----------------------------

SCORING_WEIGHTS: Dict[MatchFactor, float] = {
    MatchFactor.SKILL: 0.40,
    MatchFactor.LOCATION: 0.20,
    MatchFactor.SALARY: 0.15,
    MatchFactor.EXPERIENCE: 0.15,
    MatchFactor.ROLE: 0.10,
}


# ----------------------------
# Internal Models
# ----------------------------

@dataclass
class ScoreBreakdown:
    skill_match: float
    location_match: float
    salary_match: float
    experience_match: float
    role_match: float


@dataclass
class MatchResult:
    job_id: str
    match_score: float
    breakdown: ScoreBreakdown
    missing_skills: List[str]
    recommendation_reason: str
