import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create_calendar_event(
    start_time: str,
    start_timezone: str,
    end_time: str,
    end_timezone: str,
    summary: str,
    description: str = '',
) -> dict:
    """
    Creates a Google Calendar event.

    Args:
        start_time (str): Start time in ISO 8601 format (e.g., "2025-04-30T10:00:00").
        start_timezone (str): Timezone of the start time (e.g., "America/New_York").
        end_time (str): End time in ISO 8601 format (e.g., "2025-04-30T11:00:00").
        end_timezone (str): Timezone of the end time (e.g., "America/Los_Angeles").
        summary (str): Summary or title of the event.
        description (str): Description of the event.

    Returns:
        dict: A dictionary containing the status and event details or an error message.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    
    print(f'working directory is: {os.getcwd()}')
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      print("No valid credentials found. Please log in.")
      if creds and creds.expired and creds.refresh_token:
        print("Refreshing credentials...")
        creds.refresh(Request())
      else:
        print("Logging in...")
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        print("Saving credentials to token.json...")
        token.write(creds.to_json())    

    try:
        service = build("calendar", "v3", credentials=creds)
        

        # Create the event body
        event = {
            "summary": summary,
            "description": description,
            "start": {"dateTime": start_time, "timeZone": start_timezone},
            "end": {"dateTime": end_time, "timeZone": end_timezone},
        }

        # Insert the event into the calendar
        event = service.events().insert(calendarId='primary', body=event).execute()  

        return {
            "status": "success",
            "event": event,
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
        }
    

if __name__ == '__main__':
    
    # Example usage
    start_time = "2024-06-14T04:35:00"
    start_timezone = "Asia/Kolkata"
    end_time = "2024-06-14T06:40:00"
    end_timezone = "Asia/Dubai"
    summary = "EK 101"
    description = "Booking ABCDEF"

    result = create_calendar_event(
        start_time,
        start_timezone,
        end_time,
        end_timezone,
        summary,
        description,
    )
    
    print(result)