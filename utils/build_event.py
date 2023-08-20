from icalendar import Calendar, Event
import pytz
from datetime import datetime, timedelta


def build_event_duration(summary, description, start, duration, location,
                         freq_of_recurrence, until):
    '''
    Return an event that can be added to a calendar

    summary: summary of the event
    description: description of the event
    location: self explanatory
    start, end, stamp: These are datetime.datetime objects
    freq_of_recurrence: frequency of recurrence, string which can take the
    values daily, weekly, monthly, etc.
    until: A datetime.datetime object which signifies when the recurrence will
    end
    '''

    event = Event()
    event.add('summary', summary)
    event.add('description', description)
    event.add('dtstart', start)
    event.add('duration', timedelta(hours=duration))
    event.add('dtstamp', datetime.now())
    event.add('location', location)
    event.add('rrule', {'FREQ': freq_of_recurrence, 'UNTIL': until})

    return event


def generate_india_time(year, month, date, hour, minutes):
    return datetime(year, month, date, hour, minutes, tzinfo=pytz.timezone('Asia/Kolkata'))

