#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Clear static files and collect again
rm -rf staticfiles
echo "🔄 Coletando arquivos estáticos..."
python manage.py collectstatic --no-input --clear --verbosity=2

# Verify static files were collected
echo "📁 Verificando arquivos estáticos coletados:"
ls -la staticfiles/admin/css/ || echo "❌ Pasta admin/css não encontrada"
ls -la staticfiles/admin/js/ || echo "❌ Pasta admin/js não encontrada"

# Run all migrations (including Django core)
python manage.py makemigrations
python manage.py migrate

# Create superuser if not exists
python manage.py shell -c "
from django.contrib.auth.models import User;
User.objects.create_superuser('admin', 'admin@maratona.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('Superuser already exists')
"

# Set RENDER environment variable
export RENDER=true
