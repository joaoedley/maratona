"""
URL configuration for maratona_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.http import HttpResponse
from django.shortcuts import render
import os
import mimetypes

def frontend_view(request):
    """Serve the frontend HTML"""
    try:
        with open(settings.BASE_DIR / 'frontend' / 'index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html')
    except FileNotFoundError:
        return HttpResponse('<h1>Frontend não encontrado</h1><p>Acesse <a href="/admin/">Admin</a> ou <a href="/api/inscricoes/categorias/">API</a></p>')

def serve_static_file(request, path):
    """Serve static files with correct MIME types"""
    try:
        # Try multiple possible paths
        possible_paths = [
            os.path.join(settings.BASE_DIR, 'staticfiles', path),
            os.path.join(settings.BASE_DIR, 'static', path),
            os.path.join(settings.STATIC_ROOT, path) if settings.STATIC_ROOT else None
        ]
        
        file_path = None
        for p in possible_paths:
            if p and os.path.exists(p):
                file_path = p
                break
        
        if not file_path:
            # Debug: list available files
            debug_info = f"File not found: {path}\n"
            debug_info += f"Tried paths:\n"
            for p in possible_paths:
                if p:
                    debug_info += f"  - {p} (exists: {os.path.exists(p)})\n"
            
            # Check if staticfiles directory exists and list contents
            staticfiles_dir = os.path.join(settings.BASE_DIR, 'staticfiles')
            if os.path.exists(staticfiles_dir):
                debug_info += f"Staticfiles directory contents:\n"
                for root, dirs, files in os.walk(staticfiles_dir):
                    level = root.replace(staticfiles_dir, '').count(os.sep)
                    indent = ' ' * 2 * level
                    debug_info += f"{indent}{os.path.basename(root)}/\n"
                    subindent = ' ' * 2 * (level + 1)
                    for file in files[:10]:  # Limit to first 10 files
                        debug_info += f"{subindent}{file}\n"
                    if len(files) > 10:
                        debug_info += f"{subindent}... and {len(files) - 10} more files\n"
            
            return HttpResponse(debug_info, status=404, content_type='text/plain')
        
        # Determine MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            if path.endswith('.css'):
                mime_type = 'text/css'
            elif path.endswith('.js'):
                mime_type = 'application/javascript'
            else:
                mime_type = 'application/octet-stream'
        
        # Read and serve the file
        with open(file_path, 'rb') as f:
            content = f.read()
        
        return HttpResponse(content, content_type=mime_type)
    except Exception as e:
        return HttpResponse(f'Error serving file: {str(e)}', status=500)

def serve_css(request):
    """Serve CSS file"""
    try:
        with open(settings.BASE_DIR / 'frontend' / 'styles.css', 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/css')
    except FileNotFoundError:
        return HttpResponse('/* CSS not found */', content_type='text/css')

def serve_js(request):
    """Serve JavaScript file"""
    try:
        with open(settings.BASE_DIR / 'frontend' / 'script.js', 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='application/javascript')
    except FileNotFoundError:
        return HttpResponse('// JS not found', content_type='application/javascript')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('inscricoes.urls')),
    path('', frontend_view, name='frontend'),
    path('styles.css', serve_css, name='css'),
    path('script.js', serve_js, name='js'),
]

# Serve static and media files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
