from django.contrib import admin
from django.urls import include, path

from Cith2.register import views

urlpatterns = [
    path('', views.register, name='register'),
    path('privat/', views.start_registration, {'organisation': False}),
    path('organisation/', views.start_registration, {'organisation': True}),
    path('privat/schicken/', views.process_registration, {'organisation': False}, name='privat_registration'),
    path('organisation/schicken/', views.process_registration, {'organisation': True}, name='organisation_registration')
]
