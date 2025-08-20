#!/usr/bin/env python
"""
Script para inicializar o servidor da Maratona 2025
"""
import os
import sys
import subprocess
import time

def run_command(command, cwd=None):
    """Executar comando no terminal"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_dependencies():
    """Verificar se as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    try:
        import django
        import rest_framework
        import corsheaders
        import mercadopago
        import qrcode
        print("✅ Todas as dependências estão instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("💡 Execute: pip install -r requirements.txt")
        return False

def setup_database():
    """Configurar banco de dados"""
    print("\n📊 Configurando banco de dados...")
    
    # Fazer migrações
    success, stdout, stderr = run_command("python manage.py makemigrations")
    if not success:
        print(f"❌ Erro ao criar migrações: {stderr}")
        return False
    
    success, stdout, stderr = run_command("python manage.py migrate")
    if not success:
        print(f"❌ Erro ao aplicar migrações: {stderr}")
        return False
    
    print("✅ Banco de dados configurado")
    return True

def create_superuser():
    """Criar superusuário se não existir"""
    print("\n👤 Verificando superusuário...")
    
    # Verificar se já existe um superusuário
    check_cmd = 'python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())"'
    success, stdout, stderr = run_command(check_cmd)
    
    if "True" in stdout:
        print("✅ Superusuário já existe")
        return True
    
    print("📝 Criando superusuário padrão...")
    create_cmd = '''python manage.py shell -c "
from django.contrib.auth.models import User;
User.objects.create_superuser('admin', 'admin@maratona.com', 'admin123') if not User.objects.filter(username='admin').exists() else None;
print('Superusuário criado: admin/admin123')
"'''
    
    success, stdout, stderr = run_command(create_cmd)
    if success:
        print("✅ Superusuário criado - Login: admin | Senha: admin123")
        return True
    else:
        print(f"❌ Erro ao criar superusuário: {stderr}")
        return False

def start_server():
    """Iniciar servidor Django"""
    print("\n🚀 Iniciando servidor Django...")
    print("📍 Servidor será executado em: http://127.0.0.1:8000")
    print("📍 Admin: http://127.0.0.1:8000/admin")
    print("📍 API: http://127.0.0.1:8000/api/inscricoes/categorias")
    print("\n⚠️  Pressione Ctrl+C para parar o servidor")
    print("=" * 50)
    
    try:
        subprocess.run("python manage.py runserver", shell=True)
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado")

def main():
    print("🏃‍♂️ Maratona 2025 - Inicialização do Sistema")
    print("=" * 50)
    
    # Verificar dependências
    if not check_dependencies():
        return
    
    # Configurar banco de dados
    if not setup_database():
        return
    
    # Criar superusuário
    if not create_superuser():
        return
    
    print("\n✅ Sistema configurado com sucesso!")
    print("\n📋 Informações importantes:")
    print("- Frontend: http://127.0.0.1:8000")
    print("- Admin: http://127.0.0.1:8000/admin (admin/admin123)")
    print("- API: http://127.0.0.1:8000/api/inscricoes/")
    print("- Valor da inscrição: R$ 1,00")
    print("- Mercado Pago: Configurado com credenciais de teste")
    
    input("\n▶️  Pressione Enter para iniciar o servidor...")
    start_server()

if __name__ == "__main__":
    main()
