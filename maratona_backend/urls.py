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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.http import HttpResponse
from django.shortcuts import render

def frontend_view(request):
    """Serve the frontend HTML"""
    try:
        with open(settings.BASE_DIR / 'frontend' / 'index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html')
    except FileNotFoundError:
        return HttpResponse('<h1>Frontend não encontrado</h1><p>Acesse <a href="/admin/">Admin</a> ou <a href="/api/inscricoes/categorias/">API</a></p>')

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
    path('', frontend_view, name='frontend'),
    path('styles.css', serve_css, name='styles'),
    path('script.js', serve_js, name='script'),
    path('admin/', admin.site.urls),
    path('api/inscricoes/', include('inscricoes.urls')),
]

# Always serve static files (needed for production)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
