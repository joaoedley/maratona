# 1ª Primeira Corrida de Rua Amadora - Sistema de Inscrições

Sistema completo de inscrições para a **1ª Primeira Corrida de Rua Amadora** da Academia Corpo & Saúde.

## 🏃‍♂️ Sobre o Evento

- **Data**: 19 de Outubro de 2025
- **Horário**: Largada às 6h da manhã
- **Percurso**: 5KM
- **Inscrição**: R$ 60,00
- **Local**: Carnaíba-PE

## 🚀 Tecnologias Utilizadas

- **Backend**: Django 5.2.5 + Django REST Framework
- **Frontend**: HTML5, CSS3, JavaScript (Bootstrap 5)
- **Pagamento**: Integração Mercado Pago PIX
- **Database**: SQLite3
- **Deploy**: Render

## ⚡ Funcionalidades

- ✅ Sistema de inscrições online
- ✅ Categorias por faixa etária e sexo
- ✅ Pagamento via PIX com QR Code
- ✅ Confirmação automática de pagamento
- ✅ Painel administrativo Django
- ✅ Design responsivo
- ✅ API REST completa

## 🎨 Design

- **Cores**: Amarelo (#FFB800) e Preto (#1a1a1a)
- **Logo**: Academia Corpo & Saúde
- **Layout**: Moderno e responsivo

## 🛠️ Como Executar

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor
python manage.py runserver
```

## 📱 URLs

- **Frontend**: http://127.0.0.1:8000
- **Admin**: http://127.0.0.1:8000/admin
- **API**: http://127.0.0.1:8000/api/inscricoes/

## 👨‍💻 Desenvolvido por

**João Edley** - Academia Corpo & Saúde

---

## 🏃‍♂️ Funcionalidades

### Backend (Django)
- ✅ Sistema de inscrições com validação automática de categorias
- ✅ Painel administrativo completo para gerenciar inscrições
- ✅ Numeração sequencial automática (0001, 0002, etc.)
- ✅ Exportação de dados em CSV
- ✅ API REST para integração com frontend
- ✅ Integração com Mercado Pago PIX
- ✅ Geração de QR Code local
- ✅ Webhook para confirmação automática de pagamentos

### Frontend
- ✅ Design responsivo e moderno
- ✅ Seções: Sobre, Categorias, Premiações, Formulário
- ✅ Validação inteligente de categorias baseada em idade/sexo
- ✅ Fluxo completo de pagamento com QR Code
- ✅ Verificação automática de status do pagamento
- ✅ Interface intuitiva e animações suaves

### Categorias Disponíveis
- Masculino 15 a 29 anos
- Masculino 30 a 39 anos
- Masculino 40 a 49 anos
- Masculino acima de 50 anos
- Mulheres 15 a 30 anos
- Mulheres acima de 32 anos
- Categoria Geral Visitantes

## 🚀 Como Executar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar Banco de Dados
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Criar Superusuário (Admin)
```bash
python manage.py createsuperuser
```

### 4. Executar Servidor Django
```bash
python manage.py runserver
```

### 5. Abrir Frontend
Abra o arquivo `frontend/index.html` em um navegador ou sirva via servidor web.

## 🔧 Configuração

### Variáveis de Ambiente (.env)
```env
DEBUG=True
SECRET_KEY=sua-chave-secreta
MERCADO_PAGO_ACCESS_TOKEN=seu-token-mp
MERCADO_PAGO_PIX_KEY=sua-chave-pix
```

### URLs da API
- **Criar Inscrição:** `POST /api/inscricoes/criar/`
- **Processar Pagamento:** `POST /api/inscricoes/pagamento/`
- **Verificar Pagamento:** `GET /api/inscricoes/pagamento/{id}/verificar/`
- **Obter Categorias:** `GET /api/inscricoes/categorias/`
- **Webhook Mercado Pago:** `POST /api/inscricoes/webhook/mercadopago/`

## 💳 Integração Mercado Pago

O sistema utiliza as credenciais fornecidas na memória:
- **Token:** APP_USR-3935485974287001-081911-c0eed766e1650b9cee65ebd1db655bc8-416766854
- **Chave PIX:** 9bc0e344-f2ea-4315-9012-682c949a8c21
- **Webhook:** Configurado para receber notificações automáticas

## 📊 Painel Administrativo

Acesse `/admin/` para:
- Visualizar todas as inscrições
- Filtrar por status, categoria, sexo
- Exportar dados em CSV
- Marcar pagamentos como confirmados
- Editar ou remover inscrições

## 🎯 Fluxo de Inscrição

1. **Preenchimento:** Usuário preenche formulário com dados pessoais
2. **Validação:** Sistema valida categoria baseada em idade/sexo
3. **Criação:** Inscrição é criada com número sequencial
4. **Pagamento:** QR Code PIX é gerado automaticamente
5. **Confirmação:** Webhook confirma pagamento e atualiza status
6. **Finalização:** Usuário recebe confirmação da inscrição

## 🏆 Premiações

- 🥇 1° lugar: R$ 300,00
- 🥈 2° lugar: R$ 200,00  
- 🥉 3° lugar: R$ 100,00
- 🏅 Todos os participantes: Medalha de participação

## 📱 Responsividade

O frontend é totalmente responsivo e funciona perfeitamente em:
- Desktop (1920px+)
- Tablet (768px - 1024px)
- Mobile (320px - 767px)

## 🔒 Segurança

- Validação de dados no frontend e backend
- Proteção CSRF
- Configuração CORS adequada
- Webhook seguro para confirmação de pagamentos
- Sanitização de inputs

## 📝 Estrutura do Projeto

```
maratona/
├── maratona_backend/          # Configurações Django
├── inscricoes/                # App principal
│   ├── models.py             # Modelo de dados
│   ├── views.py              # Views da API
│   ├── serializers.py        # Serializers DRF
│   ├── services.py           # Serviços Mercado Pago
│   └── admin.py              # Configuração Admin
├── frontend/                  # Frontend responsivo
│   ├── index.html            # Página principal
│   ├── styles.css            # Estilos CSS
│   └── script.js             # JavaScript
├── requirements.txt           # Dependências Python
├── .env                      # Variáveis de ambiente
└── README.md                 # Este arquivo
```

## 🎨 Design

O design utiliza:
- **Bootstrap 5.3** para responsividade
- **Font Awesome 6.0** para ícones
- **Gradientes modernos** para visual atrativo
- **Animações CSS** para melhor UX
- **Cores temáticas** para corrida/esporte

## 🚨 Importante

- O valor da inscrição está fixado em **R$ 1,00**
- O evento está marcado para **19 de Outubro de 2025**
- O sistema suporta **webhook automático** do Mercado Pago
- Todas as validações são feitas tanto no frontend quanto no backend

**Deploy timestamp: 2025-08-20 22:27**

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs do Django
2. Confirme as configurações do Mercado Pago
3. Teste a conectividade da API
4. Valide as permissões do webhook
