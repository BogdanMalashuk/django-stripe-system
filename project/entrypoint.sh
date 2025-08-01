#!/bin/sh

echo "🔄 Running migrations..."
python manage.py migrate

echo "👤 Creating superuser if not exists..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@admin.com", "admin")
END

echo "🚀 Starting server..."
gunicorn project.wsgi:application --bind 0.0.0.0:8000
