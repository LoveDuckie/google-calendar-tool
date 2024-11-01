<div align="center">

# Google Calendar Tool

</div>

This tool allows you to generate a list of available time slots in your Google Calendar for the upcoming week. It integrates with the Google Calendar API to fetch events and compute free slots within working hours. The tool uses `rich_click` to provide a command-line interface.

It might do other things in the future but it was originally developed to do one thing and to do it well.

---

:warning: **NOTE:** :warning:  This was created in a couple of hours so please moderate your expectations around code-quality and any potential issues that you might find.

## Why?

This tool was built to answer the age-old question often asked by recruiters and employers when scheduling job interviews.

> "What's your availability like?"

Instead of laboriously formatting and reading my calendar for the following week, I thought it would instead be more appropriate to use a tool that would automate it for me.

### Why not use a calendar scheduling tool, like Calendly?

Surprisingly, some recruiters or employers don't like to use them or they would rather use their own in-house solution instead. This tool is meant to specifically solve instances where this problem might occur.

Using this tool offers convenience and saves time for the prospective employer and the candidate (presumably you, the person reading this).

## Demonstration

<div align="center">

![google-calendar-tool demonstration](<assets/gcal-tool-generate.gif>)

</div>

## Requirements

1. An account with Google Cloud Platform.
2. OAuth2 access to the account with the calendar.

## Installation

1. Clone the repository:

   ```sh
   #!/usr/bin/env bash
   git clone https://github.com/LoveDuckie/google-calendar-tool
   cd google-calendar-tool
   ```

2. Install the package:

   ```sh
   #!/usr/bin/env bash
   pip install .
   ```

3. Ensure you have the required Google Calendar API credentials in a JSON file. You can create these by following the [Google Calendar API quickstart guide](https://developers.google.com/calendar/quickstart/python).

## Usage

### Generating Availability

The tool provides a command-line command to generate a list of availability slots from your Google Calendar. 

```sh
#!/usr/bin/env bash
gcal-tool generate [OPTIONS]
```

### Options

- `--credentials-filepath` (default: `./credentials.json`):  
  The path to where the Google API credentials JSON file is stored. You can generate this file in the Google Cloud Console.

- `--output-type` (default: `default`):  
  Specifies the output format of the generated availability. The allowed values are:
  - `default`: Prints the availability in a human-readable format.
  - `json`: Outputs the availability as a JSON object.

- `--buffer-minutes` (default: 30):  
  The buffer time in minutes to leave before and after each event to allow for preparation and transition.

### Example

To generate your availability using a custom credentials file and in JSON format:

```sh
#!/usr/bin/env bash
gcal-tool generate --credentials-filepath "/path/to/credentials.json" --output-type "json"
```

## How It Works

The `generate` command uses the Google Calendar API to retrieve events from the primary calendar of the authenticated user for the next 7 days. It then calculates free time slots in the calendar, considering a buffer of 30 minutes before and after each event.

The tool checks each working day (Monday to Friday) for availability, and prints out the available time slots in the following format:

```
Availability for Monday, October 7th:
 - Available: 09:00 to 11:30
 - Available: 14:00 to 17:00
```

### Key Functions

- **`authenticate_google_calendar(credentials_filepath: str)`**  
  Authenticates and returns a Google Calendar API service instance using the specified credentials file.

- **`get_free_slots(service, start_date, end_date)`**  
  Fetches events between `start_date` and `end_date` and calculates the available time slots for each working day.

## Dependencies

- Python 3.6+
- `google-auth`
- `google-auth-oauthlib`
- `google-api-python-client`
- `rich-click`

You can install these dependencies using:

```sh
#!/usr/bin/env bash
pip install -r requirements.txt
```

## Error Handling

The tool will raise errors for the following cases:
- If the `context` object or any required arguments are invalid.
- If the credentials file path is not defined or the file does not exist.

## Troubleshooting

Ensure you have the appropriate permissions for the Google Calendar API and that the credentials file (`credentials.json`) is valid and accessible.
