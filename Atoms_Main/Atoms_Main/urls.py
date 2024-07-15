"""
URL configuration for Atoms_Main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('Atoms_users.urls')),
    path('backend/', include('Atoms_users.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
    path('app', TemplateView.as_view(template_name='index.html')),
    path('app/dashboard', TemplateView.as_view(template_name='index.html')),
    path('app/machine', TemplateView.as_view(template_name='index.html')),
    path('app/submachine', TemplateView.as_view(template_name='index.html')),
    path('app/trail', TemplateView.as_view(template_name='index.html')),
    path('app/report', TemplateView.as_view(template_name='index.html')),
    # path('home/settings', TemplateView.as_view(template_name='index.html')),
    path('login', TemplateView.as_view(template_name='index.html')),
    path('about', TemplateView.as_view(template_name='index.html'))

]
