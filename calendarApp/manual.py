from datetime import datetime, timedelta
from .clientPlan import register

now = datetime.utcnow().isoformat() + 'Z'
finish = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'
date_start = datetime.utcnow().isoformat()
date_end = (datetime.utcnow() + timedelta(hours=24)).isoformat()
description = 'what do you want'
summary = 'WORK'
attendees = 'simpson_alex@example.net'
service = register()

event = {
    'summary': summary,
    'location': 'вулиця Іллюши Кулика, 31, Херсон, Херсонська область, 73000',
    'description': description,
    'start': {
        'dateTime': date_start,
        'timeZone': 'Europe/Kiev',
    },
    'end': {
        'dateTime': date_end,
        'timeZone': 'Europe/Kiev',
    },
    'attendees': [
        {'email': attendees},
    ],
    'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'email', 'minutes': 60},
            {'method': 'popup', 'minutes': 10},
        ],
    },
}


def create_event(data):
    start = datetime.strptime(data['start'], "%Y-%m-%dT%H:%M:%S")
    event['end']['dateTime'] = (start + timedelta(hours=2)).isoformat()
    event['start']['dateTime'] = start.isoformat()
    event['description'] = data['description']
    event_send = service.events(). \
        insert(calendarId='3heg1bu3gvoqmplmp5kpqn56ic@group.calendar.google.com', body=event).execute()
    print('Event created: %s' % (event_send.get('htmlLink')))

    return event


def get_event():
    get_event = service.events().list(calendarId='3heg1bu3gvoqmplmp5kpqn56ic@group.calendar.google.com', timeMin=now,
                                      timeMax=finish, singleEvents=True, orderBy='startTime').execute()
    events = get_event.get('items', [])
    return events
