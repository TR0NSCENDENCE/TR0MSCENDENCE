#!/usr/bin/sh

# Hosts
echo -n 'Allowed hosts (space separated): '
read DJANGO_ALLOWED_HOSTS

echo -n 'Mail OTP redirect address: '
read ORIGIN_HOSTNAME

# Django super user
echo -n 'Django superuser username: '
read DJANGO_SUPERUSER_USERNAME
echo -n 'Django superuser email: '
read DJANGO_SUPERUSER_EMAIL
echo -n 'Django superuser password: '
read -s DJANGO_SUPERUSER_PASSWORD && echo

# Database
echo -n 'Database name: '
read SQL_DATABASE
echo -n 'Database superuser username: '
read SQL_USER
echo -n 'Database superuser password: '
read -s SQL_PASSWORD && echo

# Secrets
echo -n 'Secret key: '
read -s SECRET_KEY && echo
echo -n 'Mailjet secret key: '
read -s MAILJET_SECRET_KEY && echo
echo -n 'mailjet api key: '
read -s MAILJET_API_KEY && echo
echo -n ''

echo -n > .env.prod
>>.env.prod echo DEBUG=0
>>.env.prod echo SECRET_KEY=$SECRET_KEY
>>.env.prod echo DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS
>>.env.prod echo MAILJET_SECRET_KEY=$MAILJET_SECRET_KEY
>>.env.prod echo MAILJET_API_KEY=$MAILJET_API_KEY
>>.env.prod echo ORIGIN_HOSTNAME=$ORIGIN_HOSTNAME
>>.env.prod echo DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME
>>.env.prod echo DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL
>>.env.prod echo DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD
>>.env.prod echo DJANGO_SETTINGS_MODULE=transcendance.settings
>>.env.prod echo SQL_ENGINE=django.db.backends.postgresql
>>.env.prod echo SQL_DATABASE=$SQL_DATABASE
>>.env.prod echo SQL_USER=$SQL_USER
>>.env.prod echo SQL_PASSWORD=$SQL_PASSWORD
>>.env.prod echo SQL_HOST=database
>>.env.prod echo SQL_PORT=5432
>>.env.prod echo DATABASE=postgres
>>.env.prod echo NODE_ENV=production

echo -n > .db.env.prod
>>.db.env.prod echo POSTGRES_DB=$SQL_DATABASE
>>.db.env.prod echo POSTGRES_USER=$SQL_USER
>>.db.env.prod echo POSTGRES_PASSWORD=$SQL_PASSWORD

echo 'Certificate configuration:'

cd nginx; ./gen-ca.sh
