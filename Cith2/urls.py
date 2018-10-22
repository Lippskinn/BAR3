"""Cith2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

import Cith2
from Cith2 import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', include('Cith2.search.urls')),
    path('login/', include('Cith2.login.urls')),
    path('profil/', include('Cith2.profiles.urls')),
    path('angebot/', include('Cith2.offers.urls')),
    path('registrieren/', include('Cith2.register.urls')),
    path('admin/', admin.site.urls),
    path('suchanfrage/neu/', Cith2.search.views.addQuery, name='newQuery'),
    #start Alina
    path('accounts/', include('django.contrib.auth.urls')),
    path('suchanfrage/<int:query_id>/deleteQuery/', Cith2.profiles.views.deleteQuery, name='deleteQuery'),
    #end Alina
    path('suchanfrage/<int:queryId>/bearbeiten/', Cith2.profiles.views.editQuery, name='editQuery'),
    path('suchanfrage/neu/speichern/', Cith2.search.views.addQuery, name='addQuery'),
    # start Alina
    path('admin/doc/', include('django.contrib.admindocs.urls'))
    # end Alina

]
