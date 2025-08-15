#!/bin/sh
poetry run wait-for
poetry run python manage.py migrate
exec "$@"