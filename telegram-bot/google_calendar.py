import datetime

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from config import (GOOGLE_CALENDAR_ID)


def get_current_week_events(calendar_id):
    # Load OAuth credentials
    credentials = Credentials.from_authorized_user_file('google_calendar.json')

    # Build the Google Calendar API service
    service = build('calendar', 'v3', credentials=credentials)

    # Calculate the start and end of the current week
    # today = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())
    week_end = week_start + datetime.timedelta(days=6)

    # Convert the dates to the API required format
    week_start_str = week_start.isoformat()
    week_end_str = week_end.isoformat()

    try:
        # Retrieve the events for the current week
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=week_start_str + 'T00:00:00Z',
            timeMax=week_end_str + 'T23:59:59Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        # Extract the events from the API response
        events = events_result.get('items', [])

        # Group events by day of the week
        events_by_day = {}
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_datetime = datetime.datetime.fromisoformat(start)

            # Get the week day index (0 for Monday, 1 for Tuesday, etc.)
            # week_day_index = start_datetime.weekday()

            # Get the week day name in Russian
            week_day_name = start_datetime.strftime('%A')
            week_day_russian = {
                'Monday': 'Понедельник',
                'Tuesday': 'Вторник',
                'Wednesday': 'Среда',
                'Thursday': 'Четверг',
                'Friday': 'Пятница',
                'Saturday': 'Суббота',
                'Sunday': 'Воскресенье'
            }[week_day_name]

            # Add the event to the corresponding day's list
            if week_day_russian not in events_by_day:
                events_by_day[week_day_russian] = []
            events_by_day[week_day_russian].append(event)

        # Return the events grouped by day
        return events_by_day

    except Exception as error:
        print(f'An error occurred: {error}')
        return {}


def radio_scheduler():
    calendar_id = GOOGLE_CALENDAR_ID

    # Specify the timezone
    # timezone = 'Europe/Moscow'

    # Call the function to retrieve the events for the current week
    week_events = get_current_week_events(calendar_id)

    # Create a variable to store the scheduler text
    scheduler_text = 'Сетка вещания на текущую неделю:\n\n'

    # Append the details of the events by day to the scheduler text
    for week_day, events in week_events.items():
        start_datetime = events[0]['start'].get('dateTime')
        if start_datetime:
            start_datetime = datetime.datetime.fromisoformat(start_datetime)
            date_formatted = start_datetime.strftime('%Y-%m-%d')

        scheduler_text += f'{week_day} ({date_formatted})\n' \
                          f'-----------------------------------------\n'
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_datetime = datetime.datetime.fromisoformat(start)

            # Format the event as "HH:MM => event name"
            event_name = event['summary']
            # event_formatted = start_datetime.strftime('%H:%M ' + '(' + timezone + ')' + f' => {event_name}')
            event_formatted = start_datetime.strftime(f'%H:%M => {event_name}\n')

            scheduler_text += event_formatted

        scheduler_text += '\n'

    return scheduler_text
