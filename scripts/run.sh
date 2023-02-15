#!/bin/bash

echo "Running makemigrations and migrate..."
python3 manage.py makemigrations
python3 manage.py migrate

echo "Collecting static.."
echo "yes" | python3 manage.py collectstatic

echo "Creating Superuser, Staffuser and normaluser..."
echo "from django.contrib.auth import get_user_model;\
       User = get_user_model();\
       User.objects.create_superuser('admin', 'admin@email.com', 'password');\
       User.objects.create_user('staff', 'staff@email.com', 'password',is_staff=True);\
       User.objects.create_user('user', 'user@email.com', 'password')" | python manage.py shell

#comment this line if the db already populated
echo "Populate DB"
python3 -m create_reviews   

gunicorn --bind 0.0.0.0:8000 --timeout 600 --workers 4 apps.wsgi
