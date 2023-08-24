"""
Utilities to send specific notifications
"""

from dotenv import load_dotenv
import requests
import os

# load environment variables
load_dotenv()

# get ntfy topic from environment variables
TOPIC = os.getenv("TOPIC")


def send_invalid_cookie_notif():
    # send a notification indicating that the session cookie is no longer valid
    requests.post(
        "https://ntfy.sh/" + TOPIC,
        data = "The cookie is no longer valid!",
        headers = { 
            "Title": "StaffSavvy Cookie Invalid", 
            "Priority": "4"
            }
    )


def send_x_new_available_shifts_notif(x):
    # send a notification indicating how many new shifts are available
    requests.post(
        "https://ntfy.sh/" + TOPIC,
        data = "There are " + str(x) + " new shifts are available!",
        headers = {
            "Title": "New Shifts Available!",
            "Click": "https://staff.guildofstudents.com/shifts/available"
        }
    )
