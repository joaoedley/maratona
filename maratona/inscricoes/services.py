import mercadopago
import qrcode
import base64
from io import BytesIO
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class MercadoPagoService:
    def __init__(self):
        self.sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    
    def criar_pagamento_pix(self, inscricao):
        """Criar pagamento PIX no Mercado Pago"""
        try:
            payment_data = {
                "transaction_amount": float(inscricao.valor_inscricao),
                "description": f"Inscrição Maratona 2025 - {inscricao.nome}",
                "payment_method_id": "pix",
                "payer": {
                    "email": inscricao.email,
                    "first_name": inscricao.nome.split()[0],
                    "last_name": " ".join(inscricao.nome.split()[1:]) if len(inscricao.nome.split()) > 1 else "",
                    "identification": {
                        "type": "CPF",
                        "number": "00000000000"  # Em produção, solicitar CPF
                    }
                },
                "external_reference": str(inscricao.id),
                "notification_url": "https://bf63d1fb50bf.ngrok-free.app/webhook/mercadopago/"
            }
            
            payment_response = self.sdk.payment().create(payment_data)
            
            if payment_response["status"] == 201:
                payment = payment_response["response"]
                
                # Salvar dados do pagamento na inscrição
                inscricao.mercado_pago_payment_id = payment["id"]
                
                # Gerar QR Code
                qr_code_data = payment["point_of_interaction"]["transaction_data"]["qr_code"]
                qr_code_base64 = self.gerar_qr_code_base64(qr_code_data)
                inscricao.qr_code_data = qr_code_base64
                
                inscricao.save()
                
                return {
                    "success": True,
                    "payment_id": payment["id"],
                    "qr_code": qr_code_base64,
                    "qr_code_data": qr_code_data,
                    "valor": payment["transaction_amount"]
                }
            else:
                logger.error(f"Erro ao criar pagamento: {payment_response}")
                return {
                    "success": False,
                    "error": "Erro ao processar pagamento"
                }
                
        except Exception as e:
            logger.error(f"Erro no MercadoPago: {str(e)}")
            return {
                "success": False,
                "error": f"Erro interno: {str(e)}"
            }
    
    def gerar_qr_code_base64(self, qr_data):
        """Gerar QR Code em base64"""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Converter para base64
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
            
        except Exception as e:
            logger.error(f"Erro ao gerar QR Code: {str(e)}")
            return None
    
    def verificar_pagamento(self, payment_id):
        """Verificar status do pagamento"""
        try:
            payment_response = self.sdk.payment().get(payment_id)
            
            if payment_response["status"] == 200:
                payment = payment_response["response"]
                return {
                    "status": payment["status"],
                    "status_detail": payment["status_detail"]
                }
            else:
                return None
                
        except Exception as e:
            logger.error(f"Erro ao verificar pagamento: {str(e)}")
            return None
