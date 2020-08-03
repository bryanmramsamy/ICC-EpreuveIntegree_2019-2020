#!/bin/bash

# Automatically restart the runserver_plus process if it stops with an error code
# This is for development purposes

while true; do
    if ! python3 manage.py runserver_plus 0.0.0.0:8000; then
        printf "_________________________________________________\n>>> RUNSERVER_PLUS EXITED WITH A NON-0 STATUS <<<\n>>>          Restarting in 3 seconds          <<<\n"
        sleep 3;
    else
        break
    fi
done
