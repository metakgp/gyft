from icalendar import Calendar, Event
import pytz
from datetime import datetime, timedelta


def build_event_duration(summary: str, description: str, start: datetime, duration: int, location: str,
                         freq_of_recurrence: str, until: datetime) -> Event:
    r"""
    Return an event that can be added to a calendar
    Args:
        summary: title/summary of the event
        description: description of the event
        start: datetime.datetime object of the event start time
        duration: duration in hours
        location: location of the event
        freq_of_recurrence: daily, weekly, monthly
        until: datetime.datetime object of when recurrence ends

    Returns:
        icalendar.Event object
    """

    event = Event()
    event.add('summary', summary)
    event.add('description', description)
    event.add('dtstart', start)
    event.add('duration', timedelta(hours=duration))
    event.add('dtstamp', datetime.now())
    event.add('location', location)
    event.add('rrule', {'FREQ': freq_of_recurrence, 'UNTIL': until})

    return event


# Converts time to datetime object for India/Asia/Kolkata timezone
def generate_india_time(year: int, month: int, date: int, hour: int, minutes: int) -> datetime:
  """
    Converts given time values to a datetime object with a timezone of India/Asia/Kolkata.
    
    Args:
        year (int): The year of the date.
        month (int): The month of the date.
        date (int): The day of the month.
        hour (int): The hour of the time.
        minutes (int): The minutes of the time.
        
    Returns:
        datetime: The resulting datetime object.
    """
    if not (1 <= month <= 12):
           raise ValueError("month must be between 1 and 12")
    return datetime(year, month, date, hour, minutes, tzinfo=pytz.timezone('Asia/Kolkata'))
