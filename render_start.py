#!/usr/bin/env python
"""
Script otimizado para iniciar o servidor no Render
"""
import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

def run_migrations():
    """Executar migrações antes de iniciar servidor"""
    print("🔄 Executando migrações...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maratona_backend.settings')
        django.setup()
        
        # Executar migrações
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrações executadas")
        
        # Criar superusuário se não existir
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

def main():
    """Iniciar servidor com Gunicorn para produção"""
    print("🚀 Iniciando servidor para produção (Render)")
    
    # Executar migrações primeiro
    if not run_migrations():
        print("❌ Falha nas migrações, mas continuando...")
    
    # Configurar porta do Render
    port = os.environ.get('PORT', '10000')
    
    # Usar Gunicorn para produção
    cmd = f"gunicorn --bind 0.0.0.0:{port} --workers 2 maratona_backend.wsgi:application"
    
    print(f"📍 Comando: {cmd}")
    print(f"📍 Porta: {port}")
    
    try:
        subprocess.run(cmd, shell=True)
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
