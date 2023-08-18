from __future__ import print_function
import httplib2
import os

from dates import END_TERM_BEGIN

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client import file
import json
import datetime
DEBUG = False

SCOPES = "https://www.googleapis.com/auth/calendar"
CLIENT_SECRET_FILE = "client_secret.json"
APPLICATION_NAME = "gyft"


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


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


### days to number
days = {}
days["Monday"] = 0
days["Tuesday"] = 1
days["Wednesday"] = 2
days["Thursday"] = 3
days["Friday"] = 4
days["Saturday"] = 5
###


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
            # If the event is in Nalanda, get the exact location of the classroom building/area
            if (("NR" in timetable[day][time][1] or "NC" in timetable[day][time][1]) and
                    f'{timetable[day][time][1][:2]}{timetable[day][time][1][3]}' in full_locations.keys()):
                event["location"] = full_locations[f'{timetable[day][time][1][:2]}{timetable[day][time][1][3]}']
                event["summary"] = event["summary"] + f', {timetable[day][time][1]}'
            elif timetable[day][time][1] in full_locations.keys():
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
