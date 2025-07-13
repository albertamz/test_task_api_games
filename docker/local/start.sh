#!/bin/bash
set -e

echo "🔧 Застосовуємо міграції..."
python manage.py migrate

echo "🧪 Запускаємо тести..."
pytest

echo "🚀 Стартуємо Gunicorn..."
exec gunicorn gameapi.wsgi:application --bind 0.0.0.0:8000
