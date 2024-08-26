#!/bin/sh

if [ "$DATABASE" = 'postgres' ]
then
	echo 'Waiting for postgres...'
	while ! nc -z $SQL_HOST $SQL_PORT; do
		sleep 0.1
	done
	echo 'PostgreSQL started'
fi

python manage.py makemigrations users --no-input
python manage.py makemigrations otp --no-input
python manage.py makemigrations pong --no-input
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py createsuperuser --no-input

exec "$@"
