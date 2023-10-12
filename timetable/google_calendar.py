from __future__ import print_function

import os

import httplib2
from apiclient import discovery
from oauth2client import client, file, tools
from oauth2client import file
from oauth2client import tools

from utils import END_TERM_BEGIN, SEM_BEGIN, GYFT_RECUR_STRS, get_rfc_time
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
    if not credentials or credentials.invalid:  # FIXME: credentials.invalid is unresolved but works for some reason
        flow: client.Flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials: client.Credentials = tools.run_flow(flow, store)
        print("Storing credentials to " + credential_path)
    return credentials


def create_calendar(courses: list[Course]) -> None:
    r"""
    Adds courses to Google Calendar
    Args:
        courses: list of Course objects
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)
    batch = service.new_batch_http_request()  # To add events in a batch
    for course in courses:
        event = {
            "summary": course.title,
            "location": course.get_location(),
            "start": {"dateTime": get_rfc_time(course.start_time, course.day), "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": get_rfc_time(course.end_time, course.day), "timeZone": "Asia/Kolkata"},
            "recurrence": [
                "RRULE:FREQ=WEEKLY;UNTIL={}".format(
                    END_TERM_BEGIN.strftime("%Y%m%dT000000Z")
                )
            ],
        }
        batch.add(service.events().insert(calendarId="primary", body=event))
        print("Added " + event["summary"])
    batch.execute()
    print("\nAll events added successfully!\n")


def delete_calendar():
    r"""
    Deletes all events in the calendar that recur according to schedule
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    batch = service.new_batch_http_request()  # To add events in a batch
    print('Getting the events')
    events_result = service.events().list(
        calendarId='primary', timeMin=SEM_BEGIN.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), singleEvents=False,
        timeMax=END_TERM_BEGIN.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), maxResults=2500).execute()
    events = events_result.get('items', [])
    if not events or len(events) == 0:
        print('No upcoming events found.')
        return
    for event in events:
        if event.get('recurrence', 'NoRecur') in GYFT_RECUR_STRS:
            batch.add(service.events().delete(calendarId='primary',
                                              eventId=event["id"]))
            print("Deleted: ", event["summary"], event["start"])
    batch.execute()
    print("Deletion done!")
