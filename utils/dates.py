from __future__ import print_function

import datetime

from utils import build_event
import sys

# SEM_BEGIN=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
SEM_BEGIN = build_event.generate_india_time(2023, 8, 1, 0, 0)
MID_TERM_BEGIN = build_event.generate_india_time(2023, 9, 18, 0, 0)
MID_TERM_END = build_event.generate_india_time(2023, 9, 26, 23, 59)
END_TERM_BEGIN = build_event.generate_india_time(2023, 11, 16, 0, 0)

# Adjusting dates for WORKDAYS
MID_TERM_BEGIN = MID_TERM_BEGIN.replace(day=MID_TERM_BEGIN.day - 1)
MID_TERM_END = MID_TERM_END.replace(day=MID_TERM_END.day + 1)

# Recurrence strings from above dates
GYFT_RECUR_STRS = [
    ["RRULE:FREQ=WEEKLY;UNTIL={}".format(END_TERM_BEGIN.strftime("%Y%m%dT000000Z"))],
    ["RRULE:FREQ=WEEKLY;UNTIL={}".format(MID_TERM_BEGIN.strftime("%Y%m%dT000000Z"))],
    ["RRULE:FREQ=WEEKLY;UNTIL={}".format(END_TERM_BEGIN.strftime("%Y%m%dT070000Z"))],
    ["RRULE:FREQ=WEEKLY;UNTIL={}".format(MID_TERM_BEGIN.strftime("%Y%m%dT080000Z"))],
]

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

"""
Returns a list of lists denoting the time periods of working days
"""


def get_dates() -> list[list[datetime.datetime]]:
    return [[SEM_BEGIN, MID_TERM_BEGIN], [MID_TERM_END, END_TERM_BEGIN]]


def next_weekday(current_day: datetime.datetime, weekday: str) -> datetime.datetime:
    days = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5}
    weekday = days[weekday]
    days_ahead = weekday - current_day.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return current_day + datetime.timedelta(days_ahead)


def get_rfc_time(time: int, day: str, minute: int = 0, second: int = 0) -> str:
    r"""
    Returns RFC3339 formatted time string
    Args:
        time: hour in 24-hour format
        minute:
        second:
        day: A day string from the set {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"}

    Returns: str
    """
    now = datetime.datetime.now()
    date = next_weekday(now, day)
    return date.replace(hour=time, minute=minute, second=second).__str__().replace(" ", "T")
