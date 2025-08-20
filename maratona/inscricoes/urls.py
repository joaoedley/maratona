from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.criar_inscricao, name='criar_inscricao'),
    path('pagamento/', views.processar_pagamento, name='processar_pagamento'),
    path('pagamento/<str:payment_id>/verificar/', views.verificar_pagamento, name='verificar_pagamento'),
    path('categorias/', views.obter_categorias, name='obter_categorias'),
    path('<str:numero_inscricao>/', views.obter_inscricao, name='obter_inscricao'),
    path('webhook/mercadopago/', views.webhook_mercadopago, name='webhook_mercadopago'),
]
