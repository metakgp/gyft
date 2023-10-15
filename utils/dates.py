from __future__ import print_function
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs
from utils import build_event
import sys

# SEM_BEGIN=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
SEM_BEGIN = build_event.generate_india_time(2023, 7, 31, 0, 0)
MID_TERM_BEGIN = build_event.generate_india_time(2023, 9, 18, 0, 0)
MID_TERM_END = build_event.generate_india_time(2023, 9, 26, 0, 0)
END_TERM_BEGIN = build_event.generate_india_time(2023, 11, 16, 0, 0)
AUT_BREAK_BEGIN = build_event.generate_india_time(2023, 10, 22, 0, 0)
AUT_BREAK_END = build_event.generate_india_time(2023, 10, 27, 0, 0)

# # Adjusting dates for WORKDAYS
# MID_TERM_BEGIN = MID_TERM_BEGIN.replace(day=MID_TERM_BEGIN.day - 1)
# MID_TERM_END = MID_TERM_END.replace(day=MID_TERM_END.day + 1)

# Recurrence strings from above dates
GYFT_RECUR_STRS = [
    ["RRULE:FREQ=WEEKLY;UNTIL={}".format(END_TERM_BEGIN.strftime("%Y%m%dT000000Z"))],
    ["RRULE:FREQ=WEEKLY;UNTIL={}".format(MID_TERM_BEGIN.strftime("%Y%m%dT000000Z"))],
    ["RRULE:FREQ=WEEKLY;UNTIL={}".format(END_TERM_BEGIN.strftime("%Y%m%dT070000Z"))],
    ["RRULE:FREQ=WEEKLY;UNTIL={}".format(MID_TERM_BEGIN.strftime("%Y%m%dT080000Z"))],
]


### getting holidays
def get_holidates() -> (list[datetime], list[str, datetime]):
    """
    scrapes holiday list from IITKGP website
    returns: list of holidays as occasions and datetime objects
    """
    url = "https://www.iitkgp.ac.in/holidays?lang=en"
    result = requests.get(url).text
    doc = bs(result, "html.parser")
    tbody = doc.tbody
    trs = tbody.contents
    holidays = []
    hol_dates = []
    for i in range(3, len(trs) - 7, 2):
        cnt = 0
        for tr in trs[i]:
            cnt = cnt + 1
            if cnt == 2:
                occasion = tr.string
            if cnt == 4:
                datetime_str = tr.string
                d = (int)(datetime_str[:2])
                m = (int)(datetime_str[3:5])
                y = (int)(datetime_str[6:])
                datetime_object = datetime.strptime(datetime_str, "%d.%m.20%y")
                hol_date = build_event.generate_india_time(y, m, d, 0, 0)
                holidays.append([occasion, datetime_object])
                hol_dates.append(hol_date)
    ###

    ### appending mid/end sem in holidates list
    hol_dates.extend(
        [
            SEM_BEGIN,
            MID_TERM_BEGIN,
            MID_TERM_END,
            END_TERM_BEGIN,
            AUT_BREAK_BEGIN,
            AUT_BREAK_END,
        ]
    )
    hol_dates.sort()
    return hol_dates, holidays


# print(*hol_dates, sep="\n")


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

hol_dates, holidays = get_holidates()


def get_dates() -> list[datetime, datetime]:
    """
    returns intervals of working dates
    """
    intervals = []
    for i in range(0, len(hol_dates)):
        if hol_dates[i] == MID_TERM_BEGIN:
            continue
        # if hol_dates[i] == END_TERM_BEGIN:
        #     break
        if hol_dates[i] >= AUT_BREAK_BEGIN and hol_dates[i] < AUT_BREAK_END:
            continue
        if hol_dates[i] >= SEM_BEGIN and hol_dates[i] < END_TERM_BEGIN:
            intervals.append(
                [
                    hol_dates[i],
                    hol_dates[i + 1] - timedelta(days=1),
                ]
            )
    return intervals


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
    now = datetime.now()
    date = next_weekday(now, day)
    return (
        date.replace(hour=time, minute=minute, second=second)
        .__str__()
        .replace(" ", "T")
    )
