from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
import csv
from .models import Inscricao


@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = [
        'numero_inscricao', 'nome', 'idade', 'email', 'sexo', 
        'cidade', 'categoria', 'status_pagamento_badge', 'data_inscricao'
    ]
    list_filter = ['status_pagamento', 'categoria', 'sexo', 'data_inscricao']
    search_fields = ['numero_inscricao', 'nome', 'email', 'cidade']
    readonly_fields = ['numero_inscricao', 'data_inscricao', 'data_pagamento']
    list_per_page = 50
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('numero_inscricao', 'nome', 'idade', 'email', 'sexo', 'cidade')
        }),
        ('Categoria e Pagamento', {
            'fields': ('categoria', 'valor_inscricao', 'status_pagamento')
        }),
        ('Controle do Sistema', {
            'fields': ('mercado_pago_payment_id', 'data_inscricao', 'data_pagamento'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['exportar_inscricoes', 'marcar_como_pago']
    
    def status_pagamento_badge(self, obj):
        colors = {
            'PENDENTE': '#ffc107',
            'PAGO': '#28a745',
            'CANCELADO': '#dc3545'
        }
        color = colors.get(obj.status_pagamento, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_pagamento_display()
        )
    status_pagamento_badge.short_description = 'Status'
    
    def exportar_inscricoes(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="inscricoes_maratona.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Número', 'Nome', 'Idade', 'Email', 'Sexo', 'Cidade', 
            'Categoria', 'Status Pagamento', 'Data Inscrição'
        ])
        
        for inscricao in queryset:
            writer.writerow([
                inscricao.numero_inscricao,
                inscricao.nome,
                inscricao.idade,
                inscricao.email,
                inscricao.get_sexo_display(),
                inscricao.cidade,
                inscricao.get_categoria_display(),
                inscricao.get_status_pagamento_display(),
                inscricao.data_inscricao.strftime('%d/%m/%Y %H:%M')
            ])
        
        return response
    exportar_inscricoes.short_description = "Exportar inscrições selecionadas"
    
    def marcar_como_pago(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status_pagamento='PAGO', data_pagamento=timezone.now())
        self.message_user(request, f'{updated} inscrições marcadas como pagas.')
    marcar_como_pago.short_description = "Marcar como pago"
