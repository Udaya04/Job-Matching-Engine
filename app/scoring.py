from app.utils import parse_experience

WEIGHTS = {
    "skill": 0.40,
    "location": 0.20,
    "salary": 0.15,
    "experience": 0.15,
    "role": 0.10
}

def calculate_skill_score(candidate_skills, required_skills):
    matched = set(candidate_skills) & set(required_skills)
    score = (len(matched) / len(required_skills)) * 100 if required_skills else 0
    missing = list(set(required_skills) - set(candidate_skills))
    return score, missing

def calculate_location_score(candidate_locations, job_location):
    return 100 if job_location in candidate_locations else 0

def calculate_salary_score(expected, salary_range):
    low, high = salary_range
    if low <= expected <= high:
        return 100
    elif expected < low:
        return 80
    else:
        return 50

def calculate_experience_score(candidate_exp, exp_required):
    low, high = parse_experience(exp_required)
    if low <= candidate_exp <= high:
        return 100
    elif candidate_exp < low:
        return 70
    else:
        return 60

def calculate_role_score(preferred_roles, job_title):
    return 100 if job_title in preferred_roles else 50

def compute_match(candidate, job):
    skill_score, missing_skills = calculate_skill_score(
        candidate.skills, job.required_skills
    )
    location_score = calculate_location_score(
        candidate.preferred_locations, job.location
    )
    salary_score = calculate_salary_score(
        candidate.expected_salary, job.salary_range
    )
    experience_score = calculate_experience_score(
        candidate.experience_years, job.experience_required
    )
    role_score = calculate_role_score(
        candidate.preferred_roles, job.title
    )

    final_score = (
        skill_score * WEIGHTS["skill"] +
        location_score * WEIGHTS["location"] +
        salary_score * WEIGHTS["salary"] +
        experience_score * WEIGHTS["experience"] +
        role_score * WEIGHTS["role"]
    )

    breakdown = {
        "skill_match": skill_score,
        "location_match": location_score,
        "salary_match": salary_score,
        "experience_match": experience_score,
        "role_match": role_score
    }

    reason = (
        f"Strong skill alignment with {len(job.required_skills)-len(missing_skills)}/"
        f"{len(job.required_skills)} matching skills."
    )

    return round(final_score, 2), breakdown, missing_skills, reason
