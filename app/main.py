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
app.mount("/static", StaticFiles(directory="static"), name="static")
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

    # Simple matching logic using your jobs.json
    matches = []
    for job in jobs_database:
        # Example logic: check if role matches or skills overlap
        if roles.lower() in job.get('role', '').lower():
            matches.append(job)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": matches,
        "message": f"Found {len(matches)} matches for you!"
    })