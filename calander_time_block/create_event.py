import argparse
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

def create_event(service, summary, start_time, end_time, description=None, attendees=None, tags=None, color_id=None):
    """Create a new event in Google Calendar with optional tags and color."""
    if tags:
        # If there are tags, append them to the description or create a new description with tags.
        tags_str = f"\nTags: {', '.join(tags)}"
        if description:
            description += tags_str
        else:
            description = tags_str

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

    if attendees:
        event['attendees'] = [{'email': email} for email in attendees]

    if color_id:
        event['colorId'] = color_id  # Set the color for the event

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')
    return event  # Return the created event

def modify_event(service, event_id, end_time):
    """Modify an existing event to end at the specified end time."""
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    event['end'] = {
        'dateTime': end_time.isoformat(),
        'timeZone': 'Australia/Melbourne',
    }
    updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    print(f'Event modified: {updated_event.get("htmlLink")}')

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

def parse_arguments():
    parser = argparse.ArgumentParser(description='Create a Google Calendar event.')
    parser.add_argument('summary', help='Summary or title of the event')
    parser.add_argument('duration_hours', type=int, help='Duration of the event in hours')
    parser.add_argument('--start_date', help='Start date of the event (format: dd/mm)')
    parser.add_argument('--start_time', help='Start time of the event (format: 24hr:mm)')
    parser.add_argument('--description', help='Description of the event')
    parser.add_argument('--attendees', help='Comma-separated list of attendee email addresses')
    parser.add_argument('--tags', help='Comma-separated list of tags/categories for the event')
    parser.add_argument('--break_type', help='Type of break to schedule (short, long, pause)')
    
    return parser.parse_args()

def schedule_break(service, original_event, break_type):
    """Schedule a break during an ongoing event."""
    break_durations = {'short': 5, 'long': 30, 'pause': None}  # Pause is indefinite
    now = datetime.datetime.now(ZoneInfo('Australia/Melbourne'))
    
    if break_type not in break_durations:
        print(f"Unknown break type: {break_type}")
        return
    
    original_event_end = datetime.datetime.fromisoformat(original_event['end']['dateTime']).astimezone(ZoneInfo('Australia/Melbourne'))
    remaining_duration = int((original_event_end - now).total_seconds() / 60)
    
    if break_type == 'pause':
        # For pause, create an indefinite break event
        create_event(service, 'Paused', now, original_event_end, description='Paused Event', tags=['break', 'pause'], color_id='7')  # Color ID 7 is a secondary color
    else:
        # Schedule a break and then resume the original event
        break_duration = break_durations[break_type]
        break_event_end = now + datetime.timedelta(minutes=break_duration)
        create_event(service, f'{break_type.capitalize()} Break', now, break_event_end, tags=['break', break_type], color_id='7')  # Color ID 7 is a secondary color
        
        # Schedule the resumption of the original event
        new_start_time = break_event_end
        create_event(service, original_event['summary'], new_start_time, new_start_time + datetime.timedelta(minutes=remaining_duration), description=original_event['description'], tags=['break', 'resume'])
    
    # Original event remains unchanged

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

def unpause_event(service):
    """Resume a paused event."""
    now = datetime.datetime.now(ZoneInfo('Australia/Melbourne'))
    ongoing_events = service.events().list(
        calendarId='primary',
        timeMin=now.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute().get('items', [])
    
    for event in ongoing_events:
        if 'break' in event.get('tags', []) and 'pause' in event.get('tags', []):
            remaining_duration = int((datetime.datetime.fromisoformat(event['end']['dateTime']).astimezone(ZoneInfo('Australia/Melbourne')) - now).total_seconds() / 60)
            delete_event(service, event['id'])
            create_event(service, 'Resumed Event', now, now + datetime.timedelta(minutes=remaining_duration), description='Resumed Event', tags=['break', 'resume'])
            print("Event unpaused and resumed.")
            return

    print("No paused event found.")

if __name__ == '__main__':
    args = parse_arguments()

    summary = args.summary
    duration_hours = args.duration_hours
    start_date = args.start_date
    start_time_str = args.start_time
    description = args.description
    attendees = args.attendees.split(',') if args.attendees else None
    tags = args.tags.split(',') if args.tags else None
    break_type = args.break_type 

    # Calculate event start and end times
    if start_date and start_time_str:
        start_time = parse_time(start_time_str, start_date)
    else:
        start_time = datetime.datetime.now(ZoneInfo('Australia/Melbourne'))

    end_time = start_time + datetime.timedelta(hours=duration_hours)

    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)

    if break_type:
        # Find overlapping events and schedule a break
        overlapping_events = find_overlapping_events(service, start_time, end_time)
        for event in overlapping_events:
            event_start_time = datetime.datetime.fromisoformat(event['start']['dateTime']).astimezone(ZoneInfo('Australia/Melbourne'))
            if event_start_time > datetime.datetime.now(ZoneInfo('Australia/Melbourne')) - datetime.timedelta(minutes=10):
                delete_event(service, event['id'])
            else:
                event_end_time = datetime.datetime.fromisoformat(event['end']['dateTime']).astimezone(ZoneInfo('Australia/Melbourne'))
                if event_end_time > start_time:
                    modify_event(service, event['id'], start_time)
        
        if break_type:
            # Schedule the break
            schedule_break(service, event, break_type)
    else:
        # Create the new event with tags
        create_event(service, summary, start_time, end_time, description=description, attendees=attendees, tags=tags, color_id='1')  # Color ID 1 is the default color

