from __future__ import print_function

import os

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import file
from oauth2client import tools

from utils import END_TERM_BEGIN, SEM_BEGIN, GYFT_RECUR_STRS, get_rfc_time
from timetable import Course

DEBUG = False

SCOPES = "https://www.googleapis.com/auth/calendar"
CLIENT_SECRET_FILE = "client_secret.json"
APPLICATION_NAME = "gyft"


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, ".credentials")
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "calendar-python-quickstart.json")

    store = file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print("Storing credentials to " + credential_path)
    return credentials


def create_calendar(courses: list[Course]):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)
    batch = service.new_batch_http_request()
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


# To delete events from Google Calendar
# Deletes events having summary `Class of*`
def delete_calendar():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    print('Getting the events')
    events_result = service.events().list(
        calendarId='primary', timeMin=SEM_BEGIN.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), singleEvents=False,
        timeMax=END_TERM_BEGIN.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), maxResults=2500).execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
    for event in events:
        if event.get('recurrence', 'NoRecur') in GYFT_RECUR_STRS:
            service.events().delete(calendarId='primary',
                                    eventId=event["id"]).execute()
            print("Deleted: ", event["summary"], event["start"])
    print("Deletion done!")
