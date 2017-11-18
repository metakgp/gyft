import build_event
import datetime

SEM_BEGIN=datetime.datetime.now()
#  SEM_BEGIN=build_event.generateIndiaTime(2017, 7, 16, 0, 0)

MID_TERM_BEGIN=build_event.generateIndiaTime(2017, 9, 15, 0, 0)

MID_TERM_END=build_event.generateIndiaTime(2017, 9, 25, 23, 59)

END_TERM_BEGIN=build_event.generateIndiaTime(2017, 11, 20, 23, 59)

'''
Returns a list of lists denoting the time periods of working days
'''
def get_dates():
    return [
                [ SEM_BEGIN, MID_TERM_BEGIN ],
                [ MID_TERM_END, END_TERM_BEGIN ]
           ]
