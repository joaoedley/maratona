#!/usr/bin/env python
"""
Script para forçar migrações no Render
"""
import os
import django
from django.core.management import execute_from_command_line
from django.conf import settings

def setup_django():
    """Configurar Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maratona_backend.settings')
    django.setup()

def run_migrations():
    """Executar migrações forçadamente"""
    print("🔄 Executando migrações...")
    
    try:
        # Executar makemigrations
        execute_from_command_line(['manage.py', 'makemigrations'])
        print("✅ Makemigrations executado")
        
        # Executar migrate
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrate executado")
        
        # Criar superusuário
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@maratona.com', 'admin123')
            print("✅ Superusuário criado: admin/admin123")
        else:
            print("✅ Superusuário já existe")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro nas migrações: {e}")
        return False

if __name__ == "__main__":
    setup_django()
    run_migrations()
