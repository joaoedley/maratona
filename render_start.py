#!/usr/bin/env python
"""
Script otimizado para iniciar o servidor no Render
"""
import os
import sys
import subprocess

def main():
    """Iniciar servidor com Gunicorn para produção"""
    print("🚀 Iniciando servidor para produção (Render)")
    
    # Configurar porta do Render
    port = os.environ.get('PORT', '10000')
    
    # Usar Gunicorn para produção
    cmd = f"gunicorn --bind 0.0.0.0:{port} --workers 2 maratona_backend.wsgi:application"
    
    print(f"📍 Comando: {cmd}")
    print(f"📍 Porta: {port}")
    
    try:
        subprocess.run(cmd, shell=True)
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
