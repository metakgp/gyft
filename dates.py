from __future__ import print_function

import build_event
import datetime
import pytz
import sys

# SEM_BEGIN=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
SEM_BEGIN = build_event.generateIndiaTime(2019, 7, 15, 0, 0)

MID_TERM_BEGIN = build_event.generateIndiaTime(2019, 9, 16, 0, 0)

MID_TERM_END = build_event.generateIndiaTime(2019, 9, 24, 23, 59)

END_TERM_BEGIN = build_event.generateIndiaTime(2019, 11, 18, 0, 0)

## Sanity check

sanity = [
            SEM_BEGIN < MID_TERM_BEGIN,
            MID_TERM_BEGIN < MID_TERM_END,
            MID_TERM_END < END_TERM_BEGIN
         ]

# check if anything is False
sanity_check = [item for item in sanity if not item]

if len(sanity_check) > 0:
    print("Check the dates you have entered")
    print("Note: SEM_BEGIN < MID_TERM_BEGIN < MID_TERM_END < END_TERM_BEGIN")
    sys.exit(1)

'''
Returns a list of lists denoting the time periods of working days
'''
def get_dates():
    return [
                [ SEM_BEGIN, MID_TERM_BEGIN ],
                [ MID_TERM_END, END_TERM_BEGIN ]
           ]
