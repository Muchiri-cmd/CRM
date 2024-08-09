#!/usr/bin/env bash
# Exit on error
set -o errexit
#install dependencies
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

#Create superuser
echo "CREATE_SUPERUSER: $CREATE_SUPERUSER"
echo "DJANGO_SUPERUSER_EMAIL: $DJANGO_SUPERUSER_EMAIL"
echo "DJANGO_SUPERUSER_PASSWORD: $DJANGO_SUPERUSER_PASSWORD"
echo "DJANGO_SUPERUSER_USERNAME: $DJANGO_SUPERUSER_USERNAME"

if [[ "$CREATE_SUPERUSER" == "True" ]] || [[ "$CREATE_SUPERUSER" == "true" ]]; then
  python manage.py createsuperuser --no-input
fi

# Apply any outstanding database migrations
python manage.py migrate