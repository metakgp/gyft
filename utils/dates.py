from __future__ import print_function
from datetime import datetime, timedelta, date
import sys
from utils import build_event
from utils.holidays_handler import get_holidays


SEM_BEGIN = build_event.generate_india_time(2025, 7, 16, 0, 0)
MID_TERM_BEGIN = build_event.generate_india_time(2025, 9, 18, 0, 0)
MID_TERM_END = build_event.generate_india_time(2025, 9, 26, 0, 0)
END_TERM_BEGIN = build_event.generate_india_time(2025, 11, 17, 0, 0)
AUT_BREAK_BEGIN = build_event.generate_india_time(2025, 9, 27, 0, 0)
AUT_BREAK_END = build_event.generate_india_time(2025, 10, 5, 0, 0)


def daterange(start_dt: datetime, end_dt: datetime):
    """
    Yield all dates d such that start_dt.date() <= d.date() <= end_dt.date().
    The time component is preserved from start_dt for each yielded datetime.
    """
    current = start_dt
    while current.date() <= end_dt.date():
        yield current
        current = current + timedelta(days=1)


def get_class_off_dates_in_semester() -> list[datetime]:
    """
    Build an exhaustive, sorted, deduplicated list of class-off dates within the semester window
    [SEM_BEGIN.date(), END_TERM_BEGIN.date()). Includes:
      - All institute holidays scraped (mapped to Asia/Kolkata midnight datetimes)
      - Entire mid-term exam range [MID_TERM_BEGIN, MID_TERM_END]
      - Entire autumn break range [AUT_BREAK_BEGIN, AUT_BREAK_END]
    Returns tz-aware datetimes at 00:00 Asia/Kolkata for each day off.
    """
    # Fetch holidays
    holidays = get_holidays()

    # Build from the scraped holidays and fixed ranges
    off = set()
    # Holidays that fall within the semester window (exclude artificial boundary markers)
    boundary_markers = {
        SEM_BEGIN,
        END_TERM_BEGIN,
        MID_TERM_BEGIN,
        MID_TERM_END,
        AUT_BREAK_BEGIN,
        AUT_BREAK_END,
    }
    for hd in holidays:
        if (
            SEM_BEGIN.date() <= hd[1].date() < END_TERM_BEGIN.date()
            and hd[1] not in boundary_markers
        ):
            off.add(hd[1])
    # Add mid-term inclusive dates
    for d in daterange(MID_TERM_BEGIN, MID_TERM_END):
        if SEM_BEGIN.date() <= d.date() < END_TERM_BEGIN.date():
            off.add(build_event.generate_india_time(d.year, d.month, d.day, 0, 0))
    # Add autumn break inclusive dates
    for d in daterange(AUT_BREAK_BEGIN, AUT_BREAK_END):
        if SEM_BEGIN.date() <= d.date() < END_TERM_BEGIN.date():
            off.add(build_event.generate_india_time(d.year, d.month, d.day, 0, 0))

    # Return a deterministic, sorted list
    return sorted(off)


# Sanity check
sanity = [
    SEM_BEGIN < MID_TERM_BEGIN,
    MID_TERM_BEGIN < MID_TERM_END,
    MID_TERM_END < END_TERM_BEGIN,
]
# check if anything is False
sanity_check = [item for item in sanity if not item]

if len(sanity_check) > 0:
    print("Check the dates you have entered")
    print("Note: SEM_BEGIN < MID_TERM_BEGIN < MID_TERM_END < END_TERM_BEGIN")
    sys.exit(1)

def next_weekday(current_day: datetime, weekday: str) -> datetime:
    days = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
    }
    weekday = days[weekday]
    days_ahead = weekday - current_day.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return current_day + timedelta(days_ahead)