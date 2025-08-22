from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import logging

from .models import Inscricao
from .serializers import InscricaoSerializer, PagamentoSerializer
from .services import MercadoPagoService
from .email_service import EmailService

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def criar_inscricao(request):
    """Criar nova inscrição"""
    serializer = InscricaoSerializer(data=request.data)
    
    if serializer.is_valid():
        inscricao = serializer.save()
        return Response({
            'success': True,
            'inscricao': InscricaoSerializer(inscricao).data,
            'message': 'Inscrição criada com sucesso!'
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def processar_pagamento(request):
    """Processar pagamento PIX via Mercado Pago"""
    serializer = PagamentoSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    inscricao_id = serializer.validated_data['inscricao_id']
    inscricao = get_object_or_404(Inscricao, id=inscricao_id)
    
    if inscricao.status_pagamento == 'PAGO':
        return Response({
            'success': False,
            'message': 'Esta inscrição já foi paga.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Processar pagamento via Mercado Pago
    mp_service = MercadoPagoService()
    resultado = mp_service.criar_pagamento_pix(inscricao)
    
    if resultado['success']:
        return Response({
            'success': True,
            'payment_id': resultado['payment_id'],
            'qr_code': resultado['qr_code'],
            'qr_code_data': resultado['qr_code_data'],
            'valor': resultado['valor'],
            'inscricao': InscricaoSerializer(inscricao).data
        })
    else:
        return Response({
            'success': False,
            'error': resultado['error']
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def verificar_pagamento(request, payment_id):
    """Verificar status do pagamento"""
    mp_service = MercadoPagoService()
    resultado = mp_service.verificar_pagamento(payment_id)
    
    if resultado:
        # Atualizar status da inscrição se necessário
        try:
            inscricao = Inscricao.objects.get(mercado_pago_payment_id=payment_id)
            if resultado['status'] == 'approved' and inscricao.status_pagamento != 'PAGO':
                inscricao.status_pagamento = 'PAGO'
                inscricao.data_pagamento = timezone.now()
                inscricao.save()
                
                # Enviar email de confirmação
                EmailService.enviar_confirmacao_inscricao(inscricao)
                logger.info(f"Email de confirmação enviado para inscrição {inscricao.numero_inscricao}")
        except Inscricao.DoesNotExist:
            pass
        
        return Response({
            'success': True,
            'status': resultado['status'],
            'status_detail': resultado['status_detail']
        })
    
    return Response({
        'success': False,
        'error': 'Pagamento não encontrado'
    }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['GET'])
def obter_categorias(request):
    """Obter lista de categorias disponíveis"""
    categorias = [
        {'value': choice[0], 'label': choice[1]} 
        for choice in Inscricao.CATEGORIA_CHOICES
    ]
    
    return Response({
        'success': True,
        'categorias': categorias
    })


@csrf_exempt
@api_view(['GET'])
def obter_inscricao(request, numero_inscricao):
    """Obter dados de uma inscrição pelo número"""
    try:
        inscricao = Inscricao.objects.get(numero_inscricao=numero_inscricao)
        return Response({
            'success': True,
            'inscricao': InscricaoSerializer(inscricao).data
        })
    except Inscricao.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Inscrição não encontrada'
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def webhook_mercadopago(request):
    """Webhook para receber notificações do Mercado Pago"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f"Webhook recebido: {data}")
            
            if data.get('type') == 'payment':
                payment_id = data.get('data', {}).get('id')
                
                if payment_id:
                    mp_service = MercadoPagoService()
                    resultado = mp_service.verificar_pagamento(payment_id)
                    
                    if resultado and resultado['status'] == 'approved':
                        try:
                            inscricao = Inscricao.objects.get(mercado_pago_payment_id=payment_id)
                            if inscricao.status_pagamento != 'PAGO':
                                inscricao.status_pagamento = 'PAGO'
                                inscricao.data_pagamento = timezone.now()
                                inscricao.save()
                                
                                # Enviar email de confirmação
                                EmailService.enviar_confirmacao_inscricao(inscricao)
                                logger.info(f"Pagamento confirmado e email enviado para inscrição {inscricao.numero_inscricao}")
                        except Inscricao.DoesNotExist:
                            logger.error(f"Inscrição não encontrada para payment_id: {payment_id}")
            
            return HttpResponse(status=200)
            
        except Exception as e:
            logger.error(f"Erro no webhook: {str(e)}")
            return HttpResponse(status=500)
    
    return HttpResponse(status=405)
