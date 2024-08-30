
---

# Google Calendar Event Management Script

This script interacts with the Google Calendar API to create and manage events. It allows you to create new events and manage overlapping events, including modifying or deleting them if needed.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Guide](#setup-guide)
- [Usage](#usage)
- [Examples](#examples)
- [License](#license)

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.7 or later
- `pip` (Python package installer)

You also need to have the `credentials.json` file from the Google Cloud Console. Follow the [Google Calendar API Python Quickstart](https://developers.google.com/calendar/quickstart/python) to obtain this file.

## Setup Guide

1. **Clone the repository** (if applicable) or create a new directory for your script.

    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Create a virtual environment** (recommended) and activate it:

    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install the required Python libraries**:

    ```sh
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pytz
    ```

4. **Obtain your `credentials.json` file** from the Google Cloud Console and place it in the same directory as the script.

5. **Run the script for the first time** to generate the `token.pickle` file:

    ```sh
    python create_event.py "Meeting with Team" 2
    ```

    This will open a browser window for you to authenticate and authorize the application to access your Google Calendar. Once authorized, the `token.pickle` file will be created for future use.

## Usage

To use the script, run the following command with the required arguments:

```sh
python create_event.py <summary> <duration_hours> [start_date] [start_time] [description (optional)]
```

### Arguments

- `<summary>`: The title of the event.
- `<duration_hours>`: The duration of the event in hours.
- `[start_date]` (optional): The start date of the event in `dd/mm` format. If not specified, the event will be scheduled for the current time.
- `[start_time]` (optional): The start time of the event in `24hr:mm` format. If not specified, the event will start immediately.
- `[description]` (optional): A description of the event.

### Example Commands

1. **Create a meeting with a 2-hour duration starting immediately:**

    ```sh
    python create_event.py "Team Meeting" 2
    ```

2. **Create a meeting scheduled for August 30, 2024, starting at 14:00 for 1 hour:**

    ```sh
    python create_event.py "Project Review" 1 30/08 14:00 "Discuss project milestones"
    ```

3. **Create a 30-minute meeting starting immediately and modify overlapping events if needed:**

    ```sh
    python create_event.py "Quick Sync" 0.5
    ```



---

