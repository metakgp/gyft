from __future__ import print_function

import build_event
import datetime
import pytz
import sys

# SEM_BEGIN=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
SEM_BEGIN = build_event.generateIndiaTime(2023, 1, 3, 0, 0)
MID_TERM_BEGIN = build_event.generateIndiaTime(2023, 2, 15, 0, 0)
MID_TERM_END = build_event.generateIndiaTime(2023, 2, 24, 23, 59)
END_TERM_BEGIN = build_event.generateIndiaTime(2023, 4, 18, 0, 0)

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

## Sanity check

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


def get_dates():
    return [[SEM_BEGIN, MID_TERM_BEGIN], [MID_TERM_END, END_TERM_BEGIN]]
