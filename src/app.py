"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Competitive soccer practices and inter-school matches",
        "schedule": "Mondays, Wednesdays, Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["alex@mergington.edu", "nina@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Pickup games, drills, and seasonal tournaments",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 7:00 PM",
        "max_participants": 12,
        "participants": ["tyler@mergington.edu", "maya@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["lucy@mergington.edu", "omar@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting workshops, script readings, and school productions",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 30,
        "participants": ["rachel@mergington.edu", "ben@mergington.edu"]
    },
    "Debate Team": {
        "description": "Practice formal debate, public speaking, and competition prep",
        "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["isaac@mergington.edu", "zoe@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Prepare for regional science competitions with hands-on projects",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["noah@mergington.edu", "mia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Basic email validation/normalization
    if not email or not isinstance(email, str):
        raise HTTPException(status_code=400, detail="Invalid email")
    normalized = email.strip().lower()

    activity = activities[activity_name]

    # Prevent duplicate registrations (case-insensitive)
    if normalized in (p.strip().lower() for p in activity["participants"]):
        raise HTTPException(
            status_code=400, detail="Student already registered for this activity")

    # Enforce capacity
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    activity["participants"].append(normalized)
    return {"message": f"Signed up {normalized} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants/{email}")
def remove_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Basic email validation/normalization
    if not email or not isinstance(email, str):
        raise HTTPException(status_code=400, detail="Invalid email")
    normalized = email.strip().lower()

    activity = activities[activity_name]

    # Find participant case-insensitively and remove
    for i, p in enumerate(activity["participants"]):
        if p.strip().lower() == normalized:
            activity["participants"].pop(i)
            return {"message": f"Unregistered {normalized} from {activity_name}"}

    raise HTTPException(status_code=404, detail="Participant not found")
