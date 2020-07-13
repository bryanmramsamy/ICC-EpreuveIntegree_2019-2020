#!/bin/bash

# Check if the script has been executed from the reservations/ directory
# Move the current directory to it if not in order to execute the script

FILE=../manage.py
if test -f "$FILE"; then
    cd ..
fi


# Automatically restart the runserver_plus process if it stops with an error code
# This is for development purposes

while true; do
    if ! python3 manage.py runserver_plus 0.0.0.0:8000; then
        printf "\n---------------------------------------------\n RUNSERVER_PLUS EXITED WITH A NON-0 STATUS ! \n      >>> Restarting in 5 seconds <<<      \n---------------------------------------------\n"
        sleep 5;
    else
        break
    fi
done

printf "\n----------------------------------\n RUNSERVER_PLUS GRACEFULLY EXITED \n----------------------------------\n"
