from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Inscricao(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    
    CATEGORIA_CHOICES = [
        ('M_15_29', 'Masculino 15 a 29 anos'),
        ('M_30_39', 'Masculino 30 a 39 anos'),
        ('M_40_49', 'Masculino 40 a 49 anos'),
        ('M_50_PLUS', 'Masculino acima de 50 anos'),
        ('F_15_30', 'Mulheres 15 a 30 anos'),
        ('F_32_PLUS', 'Mulheres acima de 32 anos'),
        ('VISITANTES', 'Categoria Geral Visitantes'),
    ]
    
    STATUS_PAGAMENTO_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    numero_inscricao = models.CharField(max_length=10, unique=True, editable=False)
    nome = models.CharField(max_length=200, verbose_name='Nome Completo')
    idade = models.IntegerField(
        validators=[MinValueValidator(15), MaxValueValidator(100)],
        verbose_name='Idade'
    )
    email = models.EmailField(verbose_name='Email')
    cpf = models.CharField(max_length=14, verbose_name='CPF', default='000.000.000-00')
    rg = models.CharField(max_length=20, verbose_name='RG', default='00.000.000-0')
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, verbose_name='Sexo')
    cidade = models.CharField(max_length=100, verbose_name='Cidade')
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, verbose_name='Categoria')
    status_pagamento = models.CharField(
        max_length=20, 
        choices=STATUS_PAGAMENTO_CHOICES, 
        default='PENDENTE',
        verbose_name='Status do Pagamento'
    )
    
    # campos para controle de pagamento
    mercado_pago_payment_id = models.CharField(max_length=100, blank=True, null=True)
    qr_code_data = models.TextField(blank=True, null=True)
    valor_inscricao = models.DecimalField(max_digits=10, decimal_places=2, default=70.00)
    
    # Campos de controle
    data_inscricao = models.DateTimeField(auto_now_add=True, verbose_name='Data da Inscrição')
    data_pagamento = models.DateTimeField(blank=True, null=True, verbose_name='Data do Pagamento')
    
    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        ordering = ['numero_inscricao']
    
    def save(self, *args, **kwargs):
        if not self.numero_inscricao:
            # Gerar número sequencial
            last_inscricao = Inscricao.objects.order_by('id').last()
            if last_inscricao:
                last_number = int(last_inscricao.numero_inscricao)
                self.numero_inscricao = f"{last_number + 1:04d}"
            else:
                self.numero_inscricao = "0001"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.numero_inscricao} - {self.nome}"
