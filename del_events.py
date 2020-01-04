# To delete events from Google Calendar
# Delets events having summary `Class of*`
from __future__ import print_function
import httplib2
import os

from dates import END_TERM_BEGIN, MID_TERM_BEGIN, SEM_BEGIN, GYFT_RECUR_STRS

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client import file
import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'gyft'


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

    store = file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=SEM_BEGIN.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), singleEvents=False, timeMax=END_TERM_BEGIN.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), maxResults=2500).execute()
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


if __name__ == '__main__':
    main()
