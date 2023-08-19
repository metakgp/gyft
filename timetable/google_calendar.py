from __future__ import print_function

import datetime
import json
import os

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import file
from oauth2client import tools

from dates import END_TERM_BEGIN, SEM_BEGIN, GYFT_RECUR_STRS

DEBUG = False

SCOPES = "https://www.googleapis.com/auth/calendar"
CLIENT_SECRET_FILE = "client_secret.json"
APPLICATION_NAME = "gyft"


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


def create_google_calendar_event(summary: str, location: str, start: str):
    pass


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


# days to number
days = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5}


def create_calendar(timetable):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    now = datetime.datetime.now()
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)
    # Get full locations of classrooms
    with open("full_location.json") as data_file:
        full_locations = json.load(data_file)
    for day in timetable:
        print("Adding events for " + day)
        startDate = next_weekday(now, days[day])
        for time in timetable[day]:
            # parsing time from time_table dict
            # currently we only parse the starting time
            # the end time might be having error of 5 minutes
            # ex. : A class ending at 17:55 might be shown ending at 18:00
            startHour = ""
            startMinute = ""
            startMeridiem = ""
            counter = 0
            for i in range(len(time)):
                if time[i] == ":":
                    counter += 1
                    continue
                if time[i] == "-":
                    break
                if counter == 0:
                    startHour += time[i]
                elif counter == 1:
                    startMinute += time[i]
                else:
                    startMeridiem += time[i]
            replaceHour = 0
            if startMeridiem == "PM":
                replaceHour += 12
            if startHour != "12":
                replaceHour += int(startHour)
            event = {}

            if timetable[day][time][3] is not None:
                event["summary"] = timetable[day][time][3].title()
            else:
                event["summary"] = timetable[day][time][0]
            if timetable[day][time][1] in full_locations.keys():
                event["location"] = full_locations[timetable[day][time][1]].title()
            else:
                event["location"] = timetable[day][time][1]
            event["start"] = {}
            start_time = startDate.replace(hour=replaceHour, minute=int(startMinute))
            event["start"]["dateTime"] = start_time.__str__().replace(" ", "T")
            event["start"]["timeZone"] = "Asia/Kolkata"
            event["end"] = {}
            event["end"]["dateTime"] = (
                (start_time + datetime.timedelta(hours=int(timetable[day][time][2])))
                .__str__()
                .replace(" ", "T")
            )
            event["end"]["timeZone"] = "Asia/Kolkata"
            event["recurrence"] = [
                "RRULE:FREQ=WEEKLY;UNTIL={}".format(
                    END_TERM_BEGIN.strftime("%Y%m%dT000000Z")
                )
            ]
            recurring_event = (
                service.events().insert(calendarId="primary", body=event).execute()
            )
            print("Added " + event["summary"])
            if DEBUG:
                print(event)
                break
        if DEBUG:
            break
    print("\n\nEvents added to calendar\n")


# To delete events from Google Calendar
# Deletes events having summary `Class of*`
def delete_calendar():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=SEM_BEGIN.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), singleEvents=False,
        timeMax=END_TERM_BEGIN.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), maxResults=2500).execute()
    events = eventsResult.get('items', [])
    # print(events)
    if not events:
        print('No upcoming events found.')
    for event in events:
        # print(event.get('recurrence'))
        if event.get('recurrence', 'NoRecur') in GYFT_RECUR_STRS:
            service.events().delete(calendarId='primary',
                                    eventId=event["id"]).execute()
            print("Deleted: ", event["summary"], event["start"])
    print("Deletion done!")
