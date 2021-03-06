#!/bin/bash

while true; do
    python manage.py db migrate
    python manage.py db upgrade

    if [[ "$?" == "0" ]]; then
        break
    fi

    echo "Initialization failed, retrying in 5 seconds..."
    sleep 5
done

exec gunicorn --workers=4 --bind 0.0.0.0:5000 wsgi:app --reload --access-logfile - --error-logfile - --timeout 30 --keep-alive 5