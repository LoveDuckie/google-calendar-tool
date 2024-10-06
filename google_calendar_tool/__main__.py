"""

"""
from __future__ import print_function

import datetime
import os.path

import rich_click as click
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


@click.group(help="The base command-line interface for the tool.")
@click.pass_context
def cli(context: click.Context) -> None:
    """

    :param context:
    :return:
    """
    if not context:
        raise ValueError("The context is invalid or null")


@cli.command("generate", help="Generate the availability list.")
@click.option("--credentials-filepath", type=str, default=os.path.join(os.getcwd(), "credentials.json"),
              help="The path to where the API credentials are stored.")
@click.pass_context
def cli_generate(context: click.Context, credentials_filepath: str) -> None:
    """
    :param context: The context object which holds state of the CLI.
    :param credentials_filepath: The path to where the API credentials are stored.
    :return: None
    """
    service = authenticate_google_calendar(credentials_filepath)
    start_of_week = datetime.datetime.now(datetime.timezone.utc)
    end_of_week = start_of_week + datetime.timedelta(days=7)

    get_free_slots(service, start_of_week, end_of_week)


# If modifying these SCOPES, delete the file token.json
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def authenticate_google_calendar(credentials_filepath: str = os.path.join(os.getcwd(), "credentials.json")):
    """
    :param credentials_filepath: The file path to the Google API credentials JSON file.
    :return: An authorized Google Calendar API service instance.
    """
    credentials = None
    # Check if token.json exists (user authentication data)
    token_filepath = os.path.join(os.getcwd(), 'token.json')
    if os.path.exists(token_filepath):
        with open(token_filepath, 'rb') as token:
            credentials = Credentials.from_authorized_user_file(token_filepath, SCOPES)

    # If there are no valid credentials, authenticate again
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            if not credentials_filepath:
                raise ValueError("The credentials file path was not defined. Unable to continue.")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_filepath, SCOPES)
            credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    return build('calendar', 'v3', credentials=credentials)

BUFFER_MINUTES = 30

def get_free_slots(service, start_date, end_date):
    """
    :param service: The service object used to interact with the calendar API.
    :param start_date: The start date of the range to find free slots within, as a datetime object.
    :param end_date: The end date of the range to find free slots within, as a datetime object.
    :return: None. The function prints the free time slots for each working day within the date range.
    """
    working_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    current_date = start_date

    # Iterate through each working day
    while current_date <= end_date:
        if current_date.strftime('%A') in working_days:
            # Set datetime to be timezone-aware (UTC)
            day_start_dt = current_date.replace(hour=0, minute=0, second=0, microsecond=0,
                                                tzinfo=datetime.timezone.utc).isoformat()
            day_end_dt = current_date.replace(hour=23, minute=59, second=59, microsecond=0,
                                              tzinfo=datetime.timezone.utc).isoformat()

            print(f"Requesting events from {day_start_dt} to {day_end_dt}")

            events_result = service.events().list(calendarId='primary',
                                                  # 'primary' refers to the main calendar of the authenticated user
                                                  timeMin=day_start_dt,
                                                  timeMax=day_end_dt,
                                                  singleEvents=True,
                                                  orderBy='startTime').execute()
            events: list = events_result.get('items', [])

            print(f"Availability for {current_date.strftime('%A, %B %d')}:")

            # If there are no events
            if not events:
                print(" - All day available")
            else:
                available_start_dt = datetime.datetime.fromisoformat(day_start_dt)

                # Iterate through events to determine free slots
                for event in events:
                    if 'dateTime' not in event['start']:
                        continue
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    end = event['end'].get('dateTime', event['end'].get('date'))
                    start_dt = datetime.datetime.fromisoformat(start) - datetime.timedelta(minutes=BUFFER_MINUTES)
                    end_dt = datetime.datetime.fromisoformat(end)

                    if available_start_dt < start_dt:
                        print(f" - Available: {available_start_dt.strftime('%H:%M')} to {start_dt.strftime('%H:%M')}")

                    # Set the next available start time after the current event with the buffer
                    available_start_dt = end_dt + datetime.timedelta(minutes=BUFFER_MINUTES)

                # Check for availability at the end of the day
                day_end_time_dt = datetime.datetime.fromisoformat(day_end_dt)
                if available_start_dt < day_end_time_dt:
                    print(f" - Available: {available_start_dt.strftime('%H:%M')} to {day_end_time_dt.strftime('%H:%M')}")

            print()  # Blank line for better readability

        current_date += datetime.timedelta(days=1)


if __name__ == "__main__":
    try:
        cli()
    except Exception as exc:
        pass
