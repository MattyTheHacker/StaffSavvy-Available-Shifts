#!/bin/bash

# cd to the directory the script
cd /home/pi/Documents/StaffSavvy-Available-Shifts/

# make sure the repo is up to date
git pull

# run the script
python check_available_shifts.py

# check for changes
if [[ `git status --porcelain` ]]; then
    # changes
    git add .
    git commit -m "Update available shifts"
    git push
else
    # no changes
    echo "No changes"
fi