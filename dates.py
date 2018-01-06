from __future__ import print_function

import build_event
import datetime
import pytz

SEM_BEGIN=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
#  SEM_BEGIN=build_event.generateIndiaTime(2017, 7, 16, 0, 0)

MID_TERM_BEGIN=build_event.generateIndiaTime(2018, 2, 19, 0, 0)

MID_TERM_END=build_event.generateIndiaTime(2018, 2, 27, 23, 59)

END_TERM_BEGIN=build_event.generateIndiaTime(2018, 4, 19, 0, 0)

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
    import os
    os.exit(1)

'''
Returns a list of lists denoting the time periods of working days
'''
def get_dates():
    return [
                [ SEM_BEGIN, MID_TERM_BEGIN ],
                [ MID_TERM_END, END_TERM_BEGIN ]
           ]
