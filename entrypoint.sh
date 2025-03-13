#!/bin/sh

echo "Waiting for PostgreSQL..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

python manage.py migrate

python manage.py collectstatic --noinput

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
from items.models import Category

User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "adminpassword")

# Создаем категории, если их нет
categories = ["Электроника", "Одежда", "Книги", "Игрушки"]
for category_name in categories:
    Category.objects.get_or_create(name=category_name)
EOF

exec gunicorn HomeWork5.wsgi:application --bind 0.0.0.0:8000

