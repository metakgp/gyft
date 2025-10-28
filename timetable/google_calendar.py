from __future__ import print_function
import os
import httplib2
from apiclient import discovery
from oauth2client import client, file, tools
from oauth2client import file
from oauth2client import tools
from datetime import datetime, timedelta, date
from collections import defaultdict
from icalendar import Event

from utils import (
    END_TERM_BEGIN,
    SEM_BEGIN,
    dates,
    generate_india_time,
)
from utils.holidays_handler import get_holidays
from utils import academic_calander_handler
from timetable import Course

DEBUG = False

SCOPES = "https://www.googleapis.com/auth/calendar"
CLIENT_SECRET_FILE = "client_secret.json"
APPLICATION_NAME = "gyft"


def get_credentials() -> client.Credentials:
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials
    """
    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, ".credentials")
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "calendar-python-quickstart.json")

    store = file.Storage(credential_path)
    credentials: client.Credentials = store.get()
    if (
        not credentials or credentials.invalid
    ):  # FIXME: credentials.invalid is unresolved but works for some reason
        flow: client.Flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials: client.Credentials = tools.run_flow(flow, store)
        print("Storing credentials to " + credential_path)
    return credentials


def create_calendar(courses: list[Course], is_web: bool = False) -> None:
    r"""
    Adds courses to Google Calendar
    Args:
        courses: list of Course objects
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)

    # Helper: get or create the dedicated 'IIT KGP' calendar
    def get_or_create_calendar_id(name: str = "IIT KGP", tz: str = "Asia/Kolkata") -> str:
        page_token = None
        while True:
            cl = service.calendarList().list(pageToken=page_token, maxResults=250).execute()
            for item in cl.get("items", []):
                if item.get("summary") == name and item.get("accessRole") in ("owner", "writer"):
                    return item["id"]
            page_token = cl.get("nextPageToken")
            if not page_token:
                break
        # Create if not found
        body = {"summary": name, "timeZone": tz}
        created = service.calendars().insert(body=body).execute()
        return created["id"]

    calendar_id = get_or_create_calendar_id()
    batch = service.new_batch_http_request()  # To add events in a batch

    # Build exhaustive class-off dates once
    class_off_days = dates.get_class_off_dates_in_semester()

    # Helper: first occurrence of the course weekday on/after SEM_BEGIN
    def first_occurrence_of_day(day_name: str):
        return dates.next_weekday(SEM_BEGIN, day_name)

    for course in courses:
        first_day = first_occurrence_of_day(course.day)
        lecture_begin_dt = generate_india_time(
            first_day.year, first_day.month, first_day.day, course.start_time, 0
        )
        lecture_end_dt = lecture_begin_dt + timedelta(hours=course.duration)

        # Build EXDATEs at the lecture start time for class-off days matching the course weekday
        exdate_stamps: list[str] = []
        for off_day in class_off_days:
            if off_day.weekday() == first_day.weekday():
                ex_dt = generate_india_time(
                    off_day.year, off_day.month, off_day.day, course.start_time, 0
                )
                if lecture_begin_dt <= ex_dt < END_TERM_BEGIN:
                    exdate_stamps.append(ex_dt.strftime("%Y%m%dT%H%M%S"))

        event = {
            "summary": course.title,
            "location": course.get_location(),
            "description": course.code,
            "start": {
                "dateTime": lecture_begin_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": "Asia/Kolkata",
            },
            "end": {
                "dateTime": lecture_end_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": "Asia/Kolkata",
            },
            "recurrence": [
                # Add EXDATE first if any
                *( ["EXDATE;TZID=Asia/Kolkata:" + ",".join(exdate_stamps)] if exdate_stamps else [] ),
                "RRULE:FREQ=WEEKLY;UNTIL={}".format(
                    END_TERM_BEGIN.strftime("%Y%m%dT000000Z")
                ),
            ],
        }

        batch.add(service.events().insert(calendarId=calendar_id, body=event))
        print("Added " + event["summary"])
    batch.execute()  ## execute batch of timetable

    # add holidays to calendar as all-day events (Asia/Kolkata midnight)
    for holiday in get_holidays():
        hdt = holiday[1]
        start_str = generate_india_time(hdt.year, hdt.month, hdt.day, 0, 0).strftime("%Y-%m-%dT00:00:00")
        end_dt = generate_india_time(hdt.year, hdt.month, hdt.day, 0, 0) + timedelta(days=1)
        holiday_event = {
            "summary": "INSTITUTE HOLIDAY : " + holiday[0],
            "start": {
                "dateTime": start_str,
                "timeZone": "Asia/Kolkata",
            },
            "end": {
                "dateTime": end_dt.strftime("%Y-%m-%dT00:00:00"),
                "timeZone": "Asia/Kolkata",
            },
        }
        service.events().insert(calendarId=calendar_id, body=holiday_event).execute()
    print("Added holidays")

    # add academic calendar entries as all-day events
    for entry in academic_calander_handler.get_academic_calendar(is_web):
        start_str = entry.start_date.strftime("%Y-%m-%dT00:00:00")
        end_str = entry.end_date.strftime("%Y-%m-%dT00:00:00")
        event = {
            "summary": entry.event,
            "start": {"dateTime": start_str, "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": end_str, "timeZone": "Asia/Kolkata"},
        }
        service.events().insert(calendarId=calendar_id, body=event).execute()
    print("Added academic calendar entries")

    print("\nAll events added successfully!\n")


def delete_calendar():
    r"""
    Deletes all events in the calendar that recur according to schedule
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)

    # Find the IIT KGP calendar and delete it entirely
    target_name = "IIT KGP"
    page_token = None
    calendar_id = None
    while True:
        cl = service.calendarList().list(pageToken=page_token, maxResults=250).execute()
        for item in cl.get("items", []):
            if item.get("summary") == target_name and item.get("accessRole") in ("owner", "writer"):
                calendar_id = item["id"]
                break
        if calendar_id or not cl.get("nextPageToken"):
            break
        page_token = cl.get("nextPageToken")

    if not calendar_id:
        print(f"Calendar '{target_name}' not found. Nothing to delete.")
        return

    service.calendars().delete(calendarId=calendar_id).execute()
    print(f"Calendar '{target_name}' deleted.")
