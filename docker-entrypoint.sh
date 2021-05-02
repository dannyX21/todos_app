#!/bin/bash
set -e

cd /todos_app
python manage.py makemigrations
python manage.py migrate

exec "$@"