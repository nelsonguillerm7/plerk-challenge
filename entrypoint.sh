#!/bin/sh

echo "Init commands"
python makemodules.py
echo "Module migrations builds"
sleep 5
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py transactions
python manage.py runserver 0.0.0.0:8000
exec "$@"
