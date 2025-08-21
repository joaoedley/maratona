from rest_framework import serializers
from .models import Inscricao


class InscricaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscricao
        fields = [
            'id', 'numero_inscricao', 'nome', 'idade', 'email', 'cpf', 'rg', 'sexo',
            'cidade', 'categoria', 'status_pagamento', 'valor_inscricao',
            'data_inscricao'
        ]
        read_only_fields = ['numero_inscricao', 'status_pagamento', 'data_inscricao']

    def validate_categoria(self, value):
        """Validar se a categoria está correta baseada na idade e sexo"""
        idade = self.initial_data.get('idade')
        sexo = self.initial_data.get('sexo')
        
        if not idade or not sexo:
            return value
            
        idade = int(idade)
        
        # Validações de categoria baseadas em idade e sexo
        if sexo == 'M':  # Masculino
            if 15 <= idade <= 29 and value != 'M_15_29':
                raise serializers.ValidationError("Para homens de 15-29 anos, selecione 'Masculino 15 a 29 anos'")
            elif 30 <= idade <= 39 and value != 'M_30_39':
                raise serializers.ValidationError("Para homens de 30-39 anos, selecione 'Masculino 30 a 39 anos'")
            elif 40 <= idade <= 49 and value != 'M_40_49':
                raise serializers.ValidationError("Para homens de 40-49 anos, selecione 'Masculino 40 a 49 anos'")
            elif idade >= 50 and value != 'M_50_PLUS':
                raise serializers.ValidationError("Para homens acima de 50 anos, selecione 'Masculino acima de 50 anos'")
        elif sexo == 'F':  # Feminino
            if 15 <= idade <= 30 and value != 'F_15_30':
                raise serializers.ValidationError("Para mulheres de 15-30 anos, selecione 'Mulheres 15 a 30 anos'")
            elif idade >= 32 and value != 'F_32_PLUS':
                raise serializers.ValidationError("Para mulheres acima de 32 anos, selecione 'Mulheres acima de 32 anos'")
        
        return value


class PagamentoSerializer(serializers.Serializer):
    inscricao_id = serializers.IntegerField()
    valor = serializers.DecimalField(max_digits=10, decimal_places=2, default=1.00)
