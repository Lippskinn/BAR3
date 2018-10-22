
from django.contrib import admin
from django.urls import path, include

import Cith2.register
from Cith2.profiles import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('merkliste/', views.profile, {'section': 'merkliste'}),
    path('angebote/', views.profile, {'section': 'angebote'}),
    path('angebote/<int:res_id>/verfuegbarkeit/', views.editAvailability, name="editAvailability"),
    path('bearbeiten/', views.editProfile, name="editProfile"),
    #start Alina
    path('loeschen/', views.deleteProfile, name="deleteProfile"),
    path('suchanfragen/', views.profile, {'section': 'suchanfragen'}),
    #end Alina
    ]