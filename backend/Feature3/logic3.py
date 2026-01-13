# backend/Feature3/logic3.py

import datetime
from typing import List, Dict, Optional
from zoneinfo import ZoneInfo  # Python 3.9+ for proper timezone handling

# Mumbai/IST timezone
IST = ZoneInfo("Asia/Kolkata")

# Fixed reminders - everyday except Sat & Sun
REMINDERS = [
    {"time": "04:00", "title": "Wake Up Alarm", "body": "Good Morning! Rise and shine Cutuu ♡ It's 4:00 AM sharp!", "type": "alarm"},
    {"time": "04:10", "title": "Morning Motivation", "body": "Good Morning my Cutuu, Get up, Be Ready for DSA ! 💪", "type": "notification"},
    {"time": "06:30", "title": "Rest Reminder", "body": "Take rest, you must be tired ❤️", "type": "notification"},
    {"time": "08:45", "title": "Study Vibes", "body": "From Front Bench to Back Bench go there for a reason ! 😎", "type": "notification"},
    {"time": "13:00", "title": "Lunch Time", "body": "Have Lunch Madam ji 🍛", "type": "notification"},
    {"time": "13:30", "title": "Chill Time", "body": "Take a Chill, Enjoy your time ☕", "type": "notification"},
    {"time": "19:00", "title": "Home Sweet Home", "body": "Reached Home? I MISS YOUUU JI 🥺❤️", "type": "notification"},
    {"time": "19:30", "title": "DSA Time", "body": "Solve DSA Ka Problems Quick ! 🚀", "type": "notification"},
    {"time": "21:45", "title": "Dinner Reminder", "body": "Please have dinner and don't forget to upload and send me the reel 🍽️", "type": "notification"},
    {"time": "22:15", "title": "Call Reminder", "body": "Someone is waiting for your call ! 📞💕", "type": "notification"},
]

# In-memory log of sent notifications (for simulation / debug; replace with DB)
sent_log: List[Dict] = []


def is_weekday(dt: Optional[datetime.datetime] = None) -> bool:
    """
    Returns True if the given date (or today in IST) is Monday-Friday.
    """
    if dt is None:
        dt = datetime.datetime.now(IST)
    weekday = dt.weekday()  # 0 = Monday ... 6 = Sunday
    return 0 <= weekday <= 4


def get_today_reminders() -> List[Dict]:
    """
    Returns list of reminders that should fire today (if weekday).
    Each item includes parsed datetime (today + time in IST).
    """
    if not is_weekday():
        return []

    today = datetime.date.today()
    reminders_today = []

    for r in REMINDERS:
        hour, minute = map(int, r["time"].split(":"))
        fire_dt = datetime.datetime(
            year=today.year,
            month=today.month,
            day=today.day,
            hour=hour,
            minute=minute,
            second=0,
            tzinfo=IST
        )

        reminders_today.append({
            **r,
            "fire_datetime": fire_dt,
            "fire_timestamp": int(fire_dt.timestamp()),  # unix seconds, useful for client or push
            "already_sent_today": any(
                s["body"] == r["body"] and s["date"] == today
                for s in sent_log
            )
        })

    # Sort by time
    reminders_today.sort(key=lambda x: x["fire_datetime"])

    return reminders_today


def mark_as_sent(body: str) -> None:
    """
    Simulate marking a reminder as sent today.
    In real app → call this when notification is actually delivered/clicked.
    """
    today = datetime.date.today()
    sent_log.append({"body": body, "date": today})


def get_next_alarm_time() -> Optional[Dict]:
    """
    Returns the next upcoming alarm (4:00 AM IST) - today or tomorrow.
    Useful for showing in UI or scheduling initial wake-up.
    """
    now = datetime.datetime.now(IST)
    today = now.date()

    alarm_time = datetime.datetime(
        year=today.year, month=today.month, day=today.day,
        hour=4, minute=0, second=0, tzinfo=IST
    )

    if now > alarm_time:
        # Already passed today → next day
        alarm_time += datetime.timedelta(days=1)

    return {
        "title": "Wake Up Alarm",
        "body": "Good Morning! Rise and shine Cutuu ♡ It's 4:00 AM sharp!",
        "fire_datetime": alarm_time,
        "fire_timestamp": int(alarm_time.timestamp()),
        "is_weekend": not is_weekday(alarm_time)
    }


def get_all_reminder_times() -> List[Dict]:
    """Just returns the static list for frontend display / configuration."""
    return REMINDERS


# Example usage (for testing)
if __name__ == "__main__":
    print("Is today weekday?", is_weekday())
    reminders = get_today_reminders()
    for r in reminders:
        print(f"{r['time']} → {r['body']} (sent? {r['already_sent_today']})")