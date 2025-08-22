#!/usr/bin/env python
import os
import sys
import django

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maratona_backend.settings')
django.setup()

from inscricoes.models import Inscricao
from inscricoes.email_service import EmailService

def test_email():
    """Teste do sistema de envio de emails"""
    print("🧪 Testando sistema de email...")
    
    # Buscar uma inscrição para teste
    inscricao = Inscricao.objects.first()
    
    if not inscricao:
        print("❌ Nenhuma inscrição encontrada para teste")
        print("💡 Crie uma inscrição primeiro através do site")
        return
    
    print(f"📧 Testando envio para: {inscricao.email}")
    print(f"📝 Inscrição: #{inscricao.numero_inscricao} - {inscricao.nome}")
    
    # Tentar enviar email
    try:
        sucesso = EmailService.enviar_confirmacao_inscricao(inscricao)
        
        if sucesso:
            print("✅ Email enviado com sucesso!")
            print(f"📬 Verifique a caixa de entrada de: {inscricao.email}")
        else:
            print("❌ Falha no envio do email")
            print("🔧 Verifique as configurações no arquivo .env")
            
    except Exception as e:
        print(f"❌ Erro ao enviar email: {str(e)}")
        print("🔧 Possíveis problemas:")
        print("   - Credenciais incorretas no .env")
        print("   - Senha de app não configurada")
        print("   - Verificação em 2 etapas não ativada")

if __name__ == "__main__":
    test_email()
