# backend/Feature2/logic.py

import datetime
from typing import List, Dict, Optional

# ────────────────────────────────────────────────
# In-memory storage (replace with DB like SQLAlchemy later)
# ────────────────────────────────────────────────

videos: List[Dict] = []                       # [{id: int, title: str, video_url: str, embed_iframe: str, notes: str | None}]
done_videos: set[int] = set()                 # set of video_ids that are marked as "done" by you (the creator/admin)
next_video_id: int = 1

# Quick lookup
_video_by_id: Dict[int, Dict] = {}


def _rebuild_video_lookup():
    global _video_by_id
    _video_by_id = {v['id']: v for v in videos}


# ────────────────────────────────────────────────
# Seeding: Your initial video (can add more later via add_video)
# ────────────────────────────────────────────────

def seed_initial_videos():
    """Run once to add your existing video."""
    global next_video_id

    if videos:
        return

    # Your provided video - cleaned up a bit
    # Fixed typo in link (ttps → https), standardized iframe (removed unnecessary referrerpolicy if not needed)
    initial_videos = [
        {
            "title": "ALL About ML We Studied - Exclusively for Sereena",
            "video_url": "https://www.youtube.com/embed/LuxOikE0Zp0?si=N3g5CfImtp6lQrHw",
            "embed_iframe": '<iframe width="560" height="315" src="https://www.youtube.com/embed/LuxOikE0Zp0?si=N3g5CfImtp6lQrHw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
            "notes": None  # or add notes if you have: "Summary of ML concepts covered in this session..."
        }
    ]

    for data in initial_videos:
        videos.append({
            "id": next_video_id,
            **data
        })
        next_video_id += 1

    _rebuild_video_lookup()


# ────────────────────────────────────────────────
# Core Functions
# ────────────────────────────────────────────────

def add_video(title: str, video_url: str, embed_iframe: str, notes: Optional[str] = None) -> Dict:
    """
    Add a new YouTube video entry (admin/you function).
    - video_url: usually the embed src like https://www.youtube.com/embed/VIDEO_ID?si=...
    - embed_iframe: full <iframe>...</iframe> string for direct UI rendering
    - notes: optional markdown/text notes or summary
    """
    global next_video_id

    # Basic cleanup
    title = title.strip()
    video_url = video_url.strip()
    embed_iframe = embed_iframe.strip()

    video = {
        "id": next_video_id,
        "title": title,
        "video_url": video_url,
        "embed_iframe": embed_iframe,
        "notes": notes.strip() if notes else None,
        "created_at": datetime.date.today().isoformat()
    }

    videos.append(video)
    _video_by_id[next_video_id] = video
    next_video_id += 1

    return video


def get_all_videos() -> List[Dict]:
    """Get list of all videos with done status."""
    return [
        {
            "id": v["id"],
            "title": v["title"],
            "video_url": v["video_url"],
            "embed_iframe": v["embed_iframe"],
            "notes": v.get("notes"),
            "done": v["id"] in done_videos
        }
        for v in videos
    ]


def get_video(video_id: int) -> Optional[Dict]:
    """Get single video entry with done status."""
    v = _video_by_id.get(video_id)
    if not v:
        return None
    return {
        "id": v["id"],
        "title": v["title"],
        "video_url": v["video_url"],
        "embed_iframe": v["embed_iframe"],
        "notes": v.get("notes"),
        "done": v["id"] in done_videos
    }


def mark_as_done(video_id: int) -> bool:
    """Mark a video as 'done' (watched/reviewed/processed). Returns True if successful."""
    if video_id not in _video_by_id:
        return False

    done_videos.add(video_id)
    return True


def mark_as_undone(video_id: int) -> bool:
    """Unmark a video as done."""
    if video_id in done_videos:
        done_videos.remove(video_id)
        return True
    return False


def get_channel_stats() -> Dict:
    """Simple stats for your channel content dashboard."""
    total = len(videos)
    done_count = len(done_videos)
    pending = total - done_count

    return {
        "totalVideos": total,
        "doneVideos": done_count,
        "pendingVideos": pending,
        "donePercentage": round((done_count / total * 100), 1) if total > 0 else 0.0,
        "lastAdded": videos[-1]["created_at"] if videos else None
    }


# Auto-seed on module import (dev convenience)
# In production: call from app.py once (e.g. on startup if DB empty)
seed_initial_videos()