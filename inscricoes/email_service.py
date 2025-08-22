from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Serviço para envio de emails relacionados às inscrições"""
    
    @staticmethod
    def enviar_confirmacao_inscricao(inscricao):
        """
        Envia email de confirmação de inscrição após pagamento aprovado
        
        Args:
            inscricao: Instância do modelo Inscricao
            
        Returns:
            bool: True se email foi enviado com sucesso, False caso contrário
        """
        try:
            # Dados para o template
            context = {
                'inscricao': inscricao,
                'evento': {
                    'nome': '1ª Primeira Corrida de Rua Amadora',
                    'data': '19 de Outubro de 2025',
                    'horario': '6h da manhã',
                    'local': 'Carnaíba-PE',
                    'distancia': '5 KM'
                }
            }
            
            # Renderizar templates
            html_message = render_to_string('emails/confirmacao_inscricao.html', context)
            plain_message = render_to_string('emails/confirmacao_inscricao.txt', context)
            
            # Configurar email
            subject = f'✅ Inscrição Confirmada - Maratona 2025 - #{inscricao.numero_inscricao}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [inscricao.email]
            
            # Enviar email
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=from_email,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=False
            )
            
            logger.info(f"Email de confirmação enviado para {inscricao.email} - Inscrição #{inscricao.numero_inscricao}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar email de confirmação para {inscricao.email}: {str(e)}")
            return False
    
    @staticmethod
    def enviar_lembrete_pagamento(inscricao):
        """
        Envia email de lembrete de pagamento pendente
        
        Args:
            inscricao: Instância do modelo Inscricao
            
        Returns:
            bool: True se email foi enviado com sucesso, False caso contrário
        """
        try:
            context = {
                'inscricao': inscricao,
                'evento': {
                    'nome': '1ª Primeira Corrida de Rua Amadora',
                    'data': '19 de Outubro de 2025'
                }
            }
            
            # Template simples para lembrete
            subject = f'⏰ Lembrete: Pagamento Pendente - Inscrição #{inscricao.numero_inscricao}'
            message = f"""
Olá {inscricao.nome},

Sua inscrição #{inscricao.numero_inscricao} para a 1ª Primeira Corrida de Rua Amadora está com pagamento pendente.

Para confirmar sua participação, complete o pagamento via PIX.

Dados da inscrição:
- Nome: {inscricao.nome}
- Categoria: {inscricao.get_categoria_display()}
- Valor: R$ {inscricao.valor_inscricao}

Acesse o site para finalizar seu pagamento.

Academia Corpo & Saúde
            """
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[inscricao.email],
                fail_silently=False
            )
            
            logger.info(f"Email de lembrete enviado para {inscricao.email} - Inscrição #{inscricao.numero_inscricao}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar lembrete para {inscricao.email}: {str(e)}")
            return False
