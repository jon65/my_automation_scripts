import datetime
import os
import pickle
import sys
from zoneinfo import ZoneInfo
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    """Authenticate and return Google Calendar service."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_event(service, summary, start_time, end_time, description=None):
    """Create a new event in Google Calendar."""
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Australia/Melbourne',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Australia/Melbourne',
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')

def modify_event(service, event_id, end_time):
    """Modify an existing event to end at the specified end time."""
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    event['end'] = {
        'dateTime': end_time.isoformat(),
        'timeZone': 'Australia/Melbourne',
    }
    updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    print(f'Event modified: {updated_event.get("htmlLink")}')

def delete_event(service, event_id):
    """Delete an existing event from Google Calendar."""
    service.events().delete(calendarId='primary', eventId=event_id).execute()
    print(f'Event deleted: {event_id}')

def find_overlapping_events(service, start_time, end_time):
    """Find events that overlap with the specified time range."""
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_time.isoformat(),
        timeMax=end_time.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])

def parse_time(hour_str, day_str):
    """Parse the hour and day strings to a datetime object in local timezone."""
    now = datetime.datetime.now()
    local_tz = ZoneInfo("Australia/Melbourne")
    day, month = map(int, day_str.split('/'))
    start_time = datetime.datetime(now.year, month, day, int(hour_str.split(':')[0]), int(hour_str.split(':')[1]), 0, tzinfo=local_tz)
    return start_time

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python create_event.py <summary> <duration_hours> [start_date] [start_time] [description (optional)]")
        print("Time format for start_date: dd/mm")
        print("Time format for start_time: 24hr:mm")
        sys.exit(1)

    summary = sys.argv[1]
    duration_hours = int(sys.argv[2])
    start_date = sys.argv[3] if len(sys.argv) > 3 else None
    start_time_str = sys.argv[4] if len(sys.argv) > 4 else None
    description = sys.argv[5] if len(sys.argv) > 5 else None

    # Calculate event start and end times
    if start_date and start_time_str:
        start_time = parse_time(start_time_str, start_date)
    else:
        start_time = datetime.datetime.now(ZoneInfo('Australia/Melbourne'))
    
    end_time = start_time + datetime.timedelta(hours=duration_hours)

    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)

    # Check for overlapping events
    overlapping_events = find_overlapping_events(service, start_time, end_time)
    for event in overlapping_events:
        event_start_time = datetime.datetime.fromisoformat(event['start']['dateTime']).astimezone(ZoneInfo('Australia/Melbourne'))
        if event_start_time > datetime.datetime.now(ZoneInfo('Australia/Melbourne')) - datetime.timedelta(minutes=10):
            delete_event(service, event['id'])
        else:
            event_end_time = datetime.datetime.fromisoformat(event['end']['dateTime']).astimezone(ZoneInfo('Australia/Melbourne'))
            if event_end_time > start_time:
                modify_event(service, event['id'], start_time)
    
    # Create the new event
    create_event(service, summary, start_time, end_time, description)
