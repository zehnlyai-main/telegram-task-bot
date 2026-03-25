"""Simple parser for custom reminder time inputs.

Supports:
  - "10m" / "10min" → 10 minutes
  - "2h" / "2hr"    → 2 hours
  - "1h30m"         → 90 minutes
  - "18:00"         → today/tomorrow at 18:00 (UTC+5)
  - "tomorrow 9am"  → tomorrow at 09:00 (UTC+5)
"""

import re
from datetime import datetime, timedelta, timezone

# Tashkent timezone (UTC+5)
TZ_OFFSET = timezone(timedelta(hours=5))


def parse_time(text: str) -> int | None:
    """Parse a time string and return delay in minutes, or None if unparseable."""
    text = text.strip().lower()

    # ── Pattern: "1h30m", "2h", "45m", "10min", "1hr" ──
    match = re.match(r'^(\d+)\s*h(?:r|our)?s?\s*(?:(\d+)\s*m(?:in)?s?)?$', text)
    if match:
        hours = int(match.group(1))
        mins = int(match.group(2)) if match.group(2) else 0
        return hours * 60 + mins

    match = re.match(r'^(\d+)\s*m(?:in)?s?$', text)
    if match:
        return int(match.group(1))

    # ── Pattern: "HH:MM" → specific time today/tomorrow ──
    match = re.match(r'^(\d{1,2}):(\d{2})$', text)
    if match:
        hour, minute = int(match.group(1)), int(match.group(2))
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return _minutes_until(hour, minute)

    # ── Pattern: "tomorrow 9am", "tomorrow 14:00" ──
    match = re.match(r'^tomorrow\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?$', text)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else 0
        ampm = match.group(3)
        if ampm == "pm" and hour != 12:
            hour += 12
        elif ampm == "am" and hour == 12:
            hour = 0
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return _minutes_until(hour, minute, tomorrow=True)

    # ── Pattern: "9am", "2pm", "9:30am" ──
    match = re.match(r'^(\d{1,2})(?::(\d{2}))?\s*(am|pm)$', text)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else 0
        ampm = match.group(3)
        if ampm == "pm" and hour != 12:
            hour += 12
        elif ampm == "am" and hour == 12:
            hour = 0
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return _minutes_until(hour, minute)

    return None


def _minutes_until(hour: int, minute: int, tomorrow: bool = False) -> int:
    """Calculate minutes from now until a specific time (UTC+5)."""
    now = datetime.now(TZ_OFFSET)
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

    if tomorrow:
        target += timedelta(days=1)
    elif target <= now:
        # Time already passed today, push to tomorrow
        target += timedelta(days=1)

    delta = (target - now).total_seconds() / 60
    return max(1, int(delta))
