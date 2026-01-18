import os
import json
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# --- 1. INITIALIZE APP FIRST (Fixes NameError) ---
app = FastAPI()

# --- 2. CONFIGURE PATHS ---
# Since you run from Job_engine/, these folders are in the current directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- 3. LOAD YOUR DATA ---
JOBS_FILE = os.path.join("data", "jobs.json")
try:
    with open(JOBS_FILE, "r") as f:
        jobs_database = json.load(f)
except FileNotFoundError:
    jobs_database = []
    print(f"Warning: {JOBS_FILE} not found!")

# --- 4. ROUTES ---
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/match-ui")
async def match_jobs(
    request: Request, 
    skills: str = Form(...), 
    experience_years: int = Form(...),
    locations: str = Form(...),
    roles: str = Form(...),
    expected_salary: int = Form(...)
):
    # Parse skills if they come from Tagify (JSON string)
    try:
        skills_list = [item['value'] for item in json.loads(skills)]
    except:
        skills_list = [s.strip() for s in skills.split(',')]

    # Improved matching logic with scoring
    matches = []
    for job in jobs_database:
        score = 0
        
        # Skills score: (matching skills / total entered) * 40
        matching_skills = sum(1 for skill in skills_list if any(skill.lower() in s.lower() for s in job.get('required_skills', [])))
        skill_score = (matching_skills / len(skills_list)) * 40 if skills_list else 0
        score += skill_score
        
        # Role score: 20 if any entered role word is in title
        role_words = [word.strip().lower() for word in roles.split()]
        title_words = job.get('title', '').lower().split()
        if any(word in title_words for word in role_words):
            score += 20
        
        # Location score: 20 if entered location is in job location
        if locations.lower() in job.get('location', '').lower():
            score += 20
        
        # Experience score: 10 if user experience >= min required
        exp_req = job.get('experience_required', '0-0')
        min_exp = int(exp_req.split('-')[0]) if '-' in exp_req else 0
        if experience_years >= min_exp:
            score += 10
        
        # Salary score: 10 if expected salary >= min salary
        sal_range = job.get('salary_range', [0, 0])
        min_sal = sal_range[0] if isinstance(sal_range, list) else 0
        if expected_salary >= min_sal:
            score += 10
        
        job_copy = job.copy()
        job_copy['score'] = score
        matches.append(job_copy)
    
    # Sort by score descending and take top 5
    matches.sort(key=lambda x: x['score'], reverse=True)
    matches = matches[:5]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": matches,
        "message": f"Top {len(matches)} matches found!"
    })