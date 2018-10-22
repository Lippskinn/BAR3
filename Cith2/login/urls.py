from django.contrib import admin
from django.urls import include, path

from Cith2.login import views

urlpatterns = [
    path('', views.loginview, name='login'),
    path('remindPassword/', views.remind_password, name='remind_password')
]


