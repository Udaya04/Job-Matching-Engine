import re
from typing import List, Tuple


def parse_experience(experience_str: str) -> Tuple[int, int]:
    
    try:
        numbers = re.findall(r"\d+", experience_str)
        if len(numbers) == 2:
            return int(numbers[0]), int(numbers[1])
        if len(numbers) == 1:
            val = int(numbers[0])
            return val, val
    except Exception:
        pass

    # Fallback for invalid or missing data
    return 0, 50


def normalize_text(text: str) -> str:
    """
    Normalize a single string for comparison.
    """
    return text.strip().lower()


def normalize_list(items: List[str]) -> List[str]:
    """
    Normalize a list of strings.

    Example:
    [' Python ', 'FastAPI'] -> ['python', 'fastapi']
    """
    return [normalize_text(item) for item in items if item.strip()]


def safe_percentage(part: int, whole: int) -> float:
    """
    Safely calculate percentage, preventing division by zero.
    """
    if whole == 0:
        return 0.0
    return (part / whole) * 100


def get_matched_skills(
    candidate_skills: List[str],
    required_skills: List[str]
) -> List[str]:
    """
    Return skills that match between candidate and job.
    """
    candidate_set = set(normalize_list(candidate_skills))
    required_set = set(normalize_list(required_skills))
    return list(candidate_set & required_set)


def get_missing_skills(
    candidate_skills: List[str],
    required_skills: List[str]
) -> List[str]:
    """
    Return skills required by the job but missing in candidate profile.
    """
    candidate_set = set(normalize_list(candidate_skills))
    required_set = set(normalize_list(required_skills))
    return list(required_set - candidate_set)


def is_salary_within_range(
    expected_salary: int,
    salary_range: Tuple[int, int]
) -> bool:
    """
    Check if expected salary lies within job salary range.
    """
    low, high = salary_range
    return low <= expected_salary <= high


def is_location_preferred(
    job_location: str,
    preferred_locations: List[str]
) -> bool:
    """
    Check if job location is among candidate's preferred locations.
    """
    job_location_norm = normalize_text(job_location)
    preferred_norm = normalize_list(preferred_locations)
    return job_location_norm in preferred_norm


def build_recommendation_reason(
    matched_skills_count: int,
    total_required_skills: int,
    location_match: bool,
    salary_match: bool,
    experience_match: bool,
    role_match: bool
) -> str:
    """
    Build a human-readable recommendation explanation.
    """
    reasons = [
        f"Skill match: {matched_skills_count}/{total_required_skills} skills matched."
    ]

    if location_match:
        reasons.append("Preferred location matched.")

    if salary_match:
        reasons.append("Salary expectations within range.")

    if experience_match:
        reasons.append("Experience level is suitable.")

    if role_match:
        reasons.append("Preferred role matched.")

    return " ".join(reasons)
