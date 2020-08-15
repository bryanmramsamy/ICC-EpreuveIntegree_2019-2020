#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres pumpkin database..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate

exec "$@"
