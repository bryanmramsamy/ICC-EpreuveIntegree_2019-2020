#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres database..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 1
    done

    echo "PostgreSQL started"
fi


# Migrate all migrations

python manage.py migrate


# Collect all static files

python manage.py collectstatic --no-input --clear


exec "$@"
