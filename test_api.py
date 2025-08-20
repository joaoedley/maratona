#!/usr/bin/env python
"""
Script para testar a API da Maratona 2025
"""
import requests
import json

API_BASE = 'http://127.0.0.1:8000/api/inscricoes'

def test_categorias():
    """Testar endpoint de categorias"""
    print("🔍 Testando endpoint de categorias...")
    try:
        response = requests.get(f'{API_BASE}/categorias/')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Categorias carregadas: {len(data.get('categorias', []))} categorias")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def test_inscricao():
    """Testar criação de inscrição"""
    print("\n📝 Testando criação de inscrição...")
    
    dados_teste = {
        "nome": "João Teste",
        "idade": 25,
        "email": "joao.teste@email.com",
        "sexo": "M",
        "cidade": "São Paulo",
        "categoria": "M_15_29"
    }
    
    try:
        response = requests.post(
            f'{API_BASE}/criar/',
            json=dados_teste,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Inscrição criada: {data.get('inscricao', {}).get('numero_inscricao')}")
            return data.get('inscricao', {}).get('id')
        else:
            print(f"❌ Erro: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return None

def main():
    print("🏃‍♂️ Teste da API - Maratona 2025")
    print("=" * 40)
    
    # Testar categorias
    if not test_categorias():
        print("\n❌ Falha no teste de categorias. Verifique se o servidor está rodando.")
        return
    
    # Testar inscrição
    inscricao_id = test_inscricao()
    
    if inscricao_id:
        print(f"\n🎉 Todos os testes passaram! ID da inscrição: {inscricao_id}")
    else:
        print("\n❌ Falha no teste de inscrição.")
    
    print("\n📋 Para testar manualmente:")
    print(f"- Categorias: GET {API_BASE}/categorias/")
    print(f"- Criar inscrição: POST {API_BASE}/criar/")
    print(f"- Admin: http://127.0.0.1:8000/admin/")

if __name__ == "__main__":
    main()
