from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']


def register():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendarApp.
    """
    creds = None
    if os.path.exists('credentials/calendar/token.pickle'):
        with open('credentials/calendar/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/calendar/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('credentials/calendar/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service
