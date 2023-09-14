"""
A script designed to scrape StaffSavvy and check if the user has any available shifts
users should put their cookie in the .env file
"""

# Imports
from notif_utils import *
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import os

# load environment variables
load_dotenv()

# get cookie from environment variables
cookie = os.getenv("COOKIE")

VALID_COOKIE = False


shifts_currently_available = []

def check_cookie():
    global VALID_COOKIE

    try:
        response = requests.get(
            url="https://staff.guildofstudents.com/shifts/available",
            headers={
                "cookie": cookie
            }
        )

        if response.status_code == 200:
            # check that we've not been redirected to the login page
            # look for the input with the id 'login_email'
            soup = BeautifulSoup(response.text, "html.parser")
            if soup.find("input", {"id": "login_email"}) is not None:
                print("Invalid cookie")
                
                send_invalid_cookie_notif()

                VALID_COOKIE = False
            else:
                print("Valid cookie")
                VALID_COOKIE = True
        else:
            VALID_COOKIE = False

    except Exception as e:
        print(e)
        # print(response.text)


def check_shifts():
    try:
        response = requests.get(
            url="https://staff.guildofstudents.com/shifts/available",
            headers={
                "cookie": cookie
            }
        )

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            if soup is not None:
                # get the rows of the table
                # we need the shift IDs, which are stored in the tr elements
                # format: <tr data-shift="1234">
                rows = soup.findAll('tr', {"data-shift": True})

                for row in rows:
                    shift_id = row["data-shift"]
                    shifts_currently_available.append(shift_id)

            else:
                print("No shifts available")
                return

    except Exception as e:
        print(e)
        # print(response.text)


def update_shift_file():
    # compare the file to the shifts currently available
    # if a shift is no longer available, remove it from the file
    # if a shift is available, add it to the file

    shifts_from_file = []

    new_shifts = 0

    # open the file and put the shifts into a list
    # if the file doesn't exist, create it

    try:
        with open("shifts.txt", "r") as f:
            for line in f:
                shifts_from_file.append(line.strip())
    except FileNotFoundError:
        with open("shifts.txt", "w") as f:
            pass

    # compare the shifts in the file to the shifts currently available
    # if a shift is no longer available, remove it from the file
    # if a shift is available, add it to the file
    # if the file is empty, add all the shifts to the file

    if len(shifts_from_file) == 0:
        with open("shifts.txt", "w") as f:
            for shift in shifts_currently_available:
                f.write(shift + "\n")
                print(f"Added shift {shift} to file")
                new_shifts += 1
    else:
        with open("shifts.txt", "w") as f:
            for shift in shifts_currently_available:
                if shift not in shifts_from_file:
                    f.write(shift + "\n")
                    print(f"Added shift {shift} to file")
                    new_shifts += 1
                elif shift in shifts_from_file:
                    f.write(shift + "\n")
                    print(f"Shift {shift} already in file")
                elif shift not in shifts_currently_available:
                    print(f"Removed shift {shift} from file")
                else:
                    print("idk what the fuck you did but it wasn't correct")
    
    if new_shifts > 0:
        send_x_new_available_shifts_notif(new_shifts)


if __name__ == "__main__":
    check_cookie()

    if VALID_COOKIE:
        check_shifts()
        update_shift_file()

