"""

"""
from __future__ import print_function

import datetime
import os.path
import google.auth.exceptions

import google
import rich_click as click
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

BUFFER_MINUTES = 30


@click.group(help="The base command-line interface for the tool.")
@click.pass_context
def cli(context: click.Context) -> None:
    """
    :param context: The Click context object that holds information about the command execution environment
    :return: None
    """
    if not context:
        raise ValueError("The context is invalid or null")


@cli.command("authenticate", help="Generate the availability list.")
def cli_authenticate(context: click.Context) -> None:
    if not context:
        raise ValueError("The context is invalid or null")
    return


@cli.command("generate", help="Generate the availability list.")
@click.option("--output-type", type=click.Choice(['default', 'json']), default="default",
              help="The path to where the API credentials are stored.")
@click.option("--buffer-minutes", type=int, default=BUFFER_MINUTES,
              help="The path to where the API credentials are stored.")
@click.option("--hour-start", type=int, default=9,
              help="The time of day that availability should start.")
@click.option("--hour-end", type=int, default=6,
              help="The time of day that availability should end.")
@click.option("--credentials-filepath", type=str, default=os.path.join(os.getcwd(), "credentials.json"),
              help="The path to where the API credentials are stored.")
@click.pass_context
def cli_generate(context: click.Context, credentials_filepath: str, output_type: str, buffer_minutes: int,
                 hour_start: int, hour_end: int) -> None:
    """
    :param context: The Click context object, which holds state information about the CLI runtime environment.
    :param credentials_filepath: The path to the file where Google API credentials are stored.
    :param output_type: Determines the format in which the availability list should be output; options are 'default' or 'json'.
    :param buffer_minutes: The number of buffer minutes that should be considered between available slots.
    :param hour_start: The starting hour of the day from which to generate availability.
    :param hour_end: The ending hour of the day up to which to generate availability.
    :return: None
    """
    if not context:
        raise ValueError("The context is invalid or null")
    if not output_type:
        raise ValueError("The output type is invalid or null")

    if not buffer_minutes:
        raise ValueError("The buffer minutes is invalid or null")
    service = authenticate_google_calendar(credentials_filepath)
    start_of_week = datetime.datetime.now(datetime.timezone.utc)
    end_of_week = start_of_week + datetime.timedelta(days=7)

    get_free_slots(service, start_of_week, end_of_week)


# If modifying these SCOPES, delete the file token.json
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def format_timerange(time_start: datetime.datetime, time_end: datetime.datetime) -> str | None:
    """
    Format the time range
    """
    if not time_start or not isinstance(time_start, datetime.datetime):
        raise ValueError("The time start is invalid or null")

    if not time_end or not isinstance(time_end, datetime.datetime):
        raise ValueError("The time end is invalid or null")

    return None


def authenticate_google_calendar(credentials_filepath: str = os.path.join(os.getcwd(), "credentials.json")):
    """
    Authenticate the Google Calendar API.
    :param credentials_filepath: The file path to the Google API credentials JSON file.
    :return: An authorized Google Calendar API service instance.
    """
    token_filepath = os.path.join(os.getcwd(), 'token.json')
    token_credentials = None

    # Check if token.json exists (user authentication data)
    if os.path.exists(token_filepath):
        token_credentials = Credentials.from_authorized_user_file(token_filepath, SCOPES)

    # Refresh or re-authenticate if needed
    if token_credentials and token_credentials.valid:
        # If the token is valid, return the authorized service
        return build('calendar', 'v3', credentials=token_credentials)
    elif token_credentials and token_credentials.expired and token_credentials.refresh_token:
        # Try to refresh the token if it's expired
        try:
            token_credentials.refresh(Request())
        except google.auth.exceptions.RefreshError:
            os.remove(token_filepath)  # Clear invalid token

    # Run authentication flow if no valid credentials are available
    if not token_credentials or not token_credentials.valid:
        if not os.path.exists(credentials_filepath):
            raise FileNotFoundError(f"The credentials file at \"{credentials_filepath}\" does not exist.")
        flow = InstalledAppFlow.from_client_secrets_file(credentials_filepath, SCOPES)
        token_credentials = flow.run_local_server(port=0)

        # Save the refreshed or new credentials
        with open(token_filepath, 'w') as token:
            token.write(token_credentials.to_json())

    return build('calendar', 'v3', credentials=token_credentials)


def format_date_with_ordinal(date) -> str:
    """
    Format the datetime object with an ordinal suffix for the day.
    :param date: The date object to be formatted.
    :return: A string representing the formatted date with an ordinal suffix for the day.
    """
    day = date.day
    suffix = "th" if 10 <= day % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return date.strftime(f"%A, %B {day}{suffix}")


def get_free_slots(service, start_date, end_date):
    """
    :param service: The service object used to interact with the calendar API.
    :param start_date: The start date of the range to find free slots within, as a datetime object.
    :param end_date: The end date of the range to find free slots within, as a datetime object.
    :return: None. The function prints the free time slots for each working day within the date range.
    """
    working_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    current_date = start_date

    available_times = []

    # Iterate through each working day
    while current_date <= end_date:
        if current_date.strftime('%A') in working_days:
            times_slots = []
            current_date_formatted = format_date_with_ordinal(current_date)

            # Set datetime to be timezone-aware (UTC)
            day_start = current_date.replace(hour=9, minute=0, second=0, microsecond=0,
                                             tzinfo=datetime.timezone.utc).isoformat()
            day_end = current_date.replace(hour=18, minute=0, second=0, microsecond=0,
                                           tzinfo=datetime.timezone.utc).isoformat()

            day_end_time_dt = datetime.datetime.fromisoformat(day_end)

            events_result = service.events().list(calendarId='primary',
                                                  # 'primary' refers to the main calendar of the authenticated user
                                                  timeMin=day_start,
                                                  timeMax=day_end,
                                                  singleEvents=True,
                                                  orderBy='startTime').execute()
            events: list = events_result.get('items', [])

            print(f"{format_date_with_ordinal(current_date)}:")

            # If there are no events
            if not events:
                print(" - All day available")
            else:
                available_start_dt = datetime.datetime.fromisoformat(day_start).replace(tzinfo=datetime.timezone.utc)

                # Iterate through events to determine free slots
                for event in events:
                    if 'dateTime' not in event['start']:
                        continue

                    event_start = event['start'].get('dateTime', event['start'].get('date'))
                    event_end = event['end'].get('dateTime', event['end'].get('date'))

                    event_start_dt = datetime.datetime.fromisoformat(event_start).replace(
                        tzinfo=datetime.timezone.utc) - datetime.timedelta(
                        minutes=BUFFER_MINUTES)
                    event_end_dt = datetime.datetime.fromisoformat(event_end).replace(tzinfo=datetime.timezone.utc)

                    if available_start_dt < event_start_dt:
                        available_times.append((current_date_formatted, available_start_dt, event_start_dt))
                        print(
                            f" - Available: {available_start_dt.strftime('%H:%M')} to {event_start_dt.strftime('%H:%M')}")

                    # Set the next available start time after the current event with the buffer
                    available_start_dt = event_end_dt + datetime.timedelta(minutes=BUFFER_MINUTES)

                # Check for availability at the end of the day

                if available_start_dt < day_end_time_dt:
                    available_times.append((current_date_formatted, available_start_dt, day_end_time_dt))
                    print(
                        f" - Available: {available_start_dt.strftime('%H:%M')} to {day_end_time_dt.strftime('%H:%M')}")

            print()  # Blank line for better readability

        current_date += datetime.timedelta(days=1)

    return available_times


if __name__ == "__main__":
    try:
        cli()
    except Exception as exc:
        print(f"An error occurred: {exc}")
