
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import json
import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'gyft'

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
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

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    now = datetime.datetime.now()
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    with open('data.txt') as data_file:    
        data = json.load(data_file)
    for day in data:
        startDate = next_weekday(now, days[day])
        for time in data[day]:
            startHour = ""
            startMinute = ""
            startMeridiem = ""
            counter = 0
            for i in range(len(time)):
                if (time[i] == ":"):
                    counter += 1
                    continue
                if (time[i] == "-"):
                    break
                if counter == 0:
                    startHour += time[i]
                elif counter == 1:
                    startMinute += time[i]
                else:
                    startMeridiem += time[i]
            replaceHour = 0
            if (startMeridiem == "PM"):
                replaceHour += 12
            if (startHour != "12"):
                replaceHour += int(startHour)
            event = {}
            event['summary'] = "Class of " + data[day][time][0]
            event['location'] = data[day][time][1]
            event['start'] = {}
            start_time = startDate.replace(hour = replaceHour, minute = int(startMinute))
            event['start']['dateTime'] = start_time.__str__().replace(" ", "T")
            event['start']['timeZone'] = "Asia/Kolkata"
            event['end'] = {}
            event['end']['dateTime'] = (start_time + datetime.timedelta(hours = int(data[day][time][2]))).__str__().replace(" ", "T")
            event['end']['timeZone'] = "Asia/Kolkata"
            event['recurrence'] = ['RRULE:FREQ=WEEKLY;UNTIL=20161120T000000Z']
            # print ("\t", time, data[day][time], event)
            recurring_event = service.events().insert(calendarId='primary', body=event).execute()

if __name__ == '__main__':
    main()