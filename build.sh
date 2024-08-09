#!/usr/bin/env bash
# Exit on error
set -o errexit
#install dependencies
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

#Create superuser
# if [[ "$CREATE_SUPERUSER" == "True" ]] || [[ "$CREATE_SUPERUSER" == "true" ]]; then
#   python manage.py createsuperuser --no-input
# fi

# Apply any outstanding database migrations
python manage.py migrate