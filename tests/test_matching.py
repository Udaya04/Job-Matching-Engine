from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_perfect_match():
    payload = {
        "candidate": {
            "skills": ["Python", "FastAPI"],
            "experience_years": 1,
            "preferred_locations": ["Bangalore"],
            "preferred_roles": ["Backend Developer"],
            "expected_salary": 800000,
            "education": {
                "degree": "B.Tech",
                "field": "CS",
                "cgpa": 8.5
            }
        },
        "jobs": [{
            "job_id": "J001",
            "title": "Backend Developer",
            "required_skills": ["Python", "FastAPI"],
            "experience_required": "0-2 years",
            "location": "Bangalore",
            "salary_range": [600000, 1000000],
            "company": "TechCorp"
        }]
    }

    response = client.post("/match-jobs", json=payload)
    assert response.status_code == 200
    assert response.json()[0]["match_score"] > 80

def test_location_mismatch():
    payload = {
        "candidate": {
            "skills": ["Python"],
            "experience_years": 1,
            "preferred_locations": ["Hyderabad"],
            "preferred_roles": ["Backend Developer"],
            "expected_salary": 700000,
            "education": {
                "degree": "B.Tech",
                "field": "CS",
                "cgpa": 8
            }
        },
        "jobs": [{
            "job_id": "J002",
            "title": "Backend Developer",
            "required_skills": ["Python"],
            "experience_required": "0-2 years",
            "location": "Bangalore",
            "salary_range": [600000, 900000],
            "company": "X"
        }]
    }

    response = client.post("/match-jobs", json=payload)
    assert response.json()[0]["breakdown"]["location_match"] == 0
