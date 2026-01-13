from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict

# Import logics from features
from Feature1.logic1 import (
    add_problem, get_all_problems, get_problem, mark_solved, get_dashboard_stats, seed_initial_problems
)
from Feature2.logic2 import (
    add_video, get_all_videos, get_video, mark_as_done, mark_as_undone, get_channel_stats, seed_initial_videos
)
from Feature3.logic3 import (
    get_today_reminders, get_next_alarm_time, get_all_reminder_times
)

app = FastAPI(
    title="Personal Productivity App",
    description="API for DSA learning, YouTube channel management, and daily reminders.",
    version="1.0.0"
)

# CORS Policy: Allow origins for development (e.g., React Native dev server, web frontend)
# In production, restrict to your actual domains/IPs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:19006", "*"],  # '*' for dev; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Seed initial data on startup (for in-memory; in real DB, use migrations)
@app.on_event("startup")
def startup_event():
    seed_initial_problems()
    seed_initial_videos()

# ────────────────────────────────────────────────
# Pydantic Models (for request/response validation)
# ────────────────────────────────────────────────

# Feature1: DSA
class ProblemCreate(BaseModel):
    title: str
    link: str

class ProblemResponse(BaseModel):
    id: int
    title: str
    link: str
    completed: bool

class DashboardStats(BaseModel):
    totalProblems: int
    solved: int
    solvedPercentage: float
    todaySolved: int
    dailySolved: Dict[str, int]
    recent7Days: Dict[str, int]

# Feature2: Videos
class VideoCreate(BaseModel):
    title: str
    video_url: str
    embed_iframe: str
    notes: Optional[str] = None

class VideoResponse(BaseModel):
    id: int
    title: str
    video_url: str
    embed_iframe: str
    notes: Optional[str]
    done: bool

class ChannelStats(BaseModel):
    totalVideos: int
    doneVideos: int
    pendingVideos: int
    donePercentage: float
    lastAdded: Optional[str]

# Feature3: Reminders
class Reminder(BaseModel):
    time: str
    title: str
    body: str
    type: str

class ReminderWithFireTime(Reminder):
    fire_datetime: str  # ISO format
    fire_timestamp: int
    already_sent_today: bool

class NextAlarm(BaseModel):
    title: str
    body: str
    fire_datetime: str
    fire_timestamp: int
    is_weekend: bool

# ────────────────────────────────────────────────
# Feature1 Endpoints: DSA Learning
# ────────────────────────────────────────────────

@app.get("/problems", response_model=List[ProblemResponse])
def list_problems():
    """Get all DSA problems with completion status."""
    return get_all_problems()

@app.get("/problems/{problem_id}", response_model=ProblemResponse)
def get_single_problem(problem_id: int):
    """Get a single DSA problem by ID."""
    problem = get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found")
    return problem

@app.post("/problems", response_model=ProblemResponse, status_code=status.HTTP_201_CREATED)
def create_problem(problem: ProblemCreate):
    """Admin: Add a new DSA problem."""
    # TODO: Add auth check for admin
    added = add_problem(problem.title, problem.link)
    return ProblemResponse(**added, completed=False)  # New problems start as not completed

@app.post("/solve/{problem_id}", status_code=status.HTTP_204_NO_CONTENT)
def solve_problem(problem_id: int):
    """Mark a DSA problem as solved today."""
    if not mark_solved(problem_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid problem ID or already solved today")
    return None

@app.get("/dsa-dashboard", response_model=DashboardStats)
def dsa_dashboard():
    """Get DSA learning dashboard stats."""
    return get_dashboard_stats()

# ────────────────────────────────────────────────
# Feature2 Endpoints: YouTube Channel
# ────────────────────────────────────────────────

@app.get("/videos", response_model=List[VideoResponse])
def list_videos():
    """Get all YouTube videos with done status."""
    return get_all_videos()

@app.get("/videos/{video_id}", response_model=VideoResponse)
def get_single_video(video_id: int):
    """Get a single video by ID."""
    video = get_video(video_id)
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    return video

@app.post("/videos", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
def create_video(video: VideoCreate):
    """Admin: Add a new YouTube video."""
    # TODO: Add auth check for admin
    added = add_video(video.title, video.video_url, video.embed_iframe, video.notes)
    return VideoResponse(**added, done=False)  # New videos start as not done

@app.post("/videos/{video_id}/done", status_code=status.HTTP_204_NO_CONTENT)
def mark_video_done(video_id: int):
    """Mark a video as done."""
    if not mark_as_done(video_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid video ID")
    return None

@app.post("/videos/{video_id}/undone", status_code=status.HTTP_204_NO_CONTENT)
def mark_video_undone(video_id: int):
    """Mark a video as undone."""
    if not mark_as_undone(video_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid video ID or already undone")
    return None

@app.get("/channel-stats", response_model=ChannelStats)
def channel_dashboard():
    """Get YouTube channel stats."""
    return get_channel_stats()

# ────────────────────────────────────────────────
# Feature3 Endpoints: Daily Reminders
# ────────────────────────────────────────────────

@app.get("/reminders/today", response_model=List[ReminderWithFireTime])
def today_reminders():
    """Get today's reminders (empty on weekends)."""
    return get_today_reminders()

@app.get("/next-alarm", response_model=NextAlarm)
def next_alarm():
    """Get the next upcoming 4:00 AM alarm details."""
    return get_next_alarm_time()

@app.get("/reminders", response_model=List[Reminder])
def all_reminders():
    """Get the static list of all reminder templates."""
    return get_all_reminder_times()

# ────────────────────────────────────────────────
# Health Check
# ────────────────────────────────────────────────

@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy"}