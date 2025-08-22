#!/usr/bin/env python
"""
Script para debugar problemas de email em produção
Execute no Render via Shell ou localmente apontando para produção
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maratona_backend.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_email_config():
    """Debug das configurações de email"""
    print("🔧 CONFIGURAÇÕES DE EMAIL:")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NÃO CONFIGURADO'}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"DEBUG: {settings.DEBUG}")
    print()

def test_simple_email():
    """Teste simples de envio de email"""
    print("📧 TESTANDO ENVIO DE EMAIL SIMPLES...")
    
    try:
        send_mail(
            subject='Teste de Email - Maratona Sistema',
            message='Este é um teste do sistema de email da maratona.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['edleyjoao@gmail.com'],
            fail_silently=False
        )
        print("✅ Email enviado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar email: {str(e)}")
        print(f"Tipo do erro: {type(e).__name__}")
        return False

def test_email_service():
    """Teste usando o EmailService"""
    print("🔧 TESTANDO EmailService...")
    
    try:
        from inscricoes.models import Inscricao
        from inscricoes.email_service import EmailService
        
        # Buscar primeira inscrição
        inscricao = Inscricao.objects.first()
        if not inscricao:
            print("❌ Nenhuma inscrição encontrada para teste")
            return False
            
        print(f"📝 Testando com inscrição: {inscricao.numero_inscricao} - {inscricao.nome}")
        
        sucesso = EmailService.enviar_confirmacao_inscricao(inscricao)
        
        if sucesso:
            print("✅ EmailService funcionou!")
            return True
        else:
            print("❌ EmailService falhou")
            return False
            
    except Exception as e:
        print(f"❌ Erro no EmailService: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 DEBUG DE EMAIL - SISTEMA MARATONA")
    print("=" * 50)
    
    debug_email_config()
    
    print("1️⃣ Teste simples de email...")
    test_simple_email()
    print()
    
    print("2️⃣ Teste do EmailService...")
    test_email_service()
    print()
    
    print("🏁 Debug concluído!")
