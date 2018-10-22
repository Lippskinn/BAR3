
from django.contrib import admin
from django.urls import path, include, re_path

import Cith2
from Cith2.offers import views

urlpatterns = [
    path('<int:id>/', views.single, name='single'),
    path('neu/', views.newOffer, name='newOffer'),
    path('<int:ObjId>/bearbeiten/', views.editOffer, name='editOffer'),
    path('<int:resource_id>/watch/', Cith2.profiles.views.watch, name='watch'),
    #start Alina
    path('<int:resource_id>/unwatch/', Cith2.profiles.views.unwatch, name='unwatch'),
    path('<int:resource_id>/deleteOffer/', Cith2.offers.views.deleteOffer, name='deleteOffer'),
    #end Alina
    path('deleteConstraint/<int:constraint_id>/', Cith2.offers.views.deleteConstraint,
         name='deleteConstraint'),
    path('<int:resource_id>/addConstraint/<slug:startDate>/<slug:endDate>/', views.addConstraint, name='addConstraint'),
]
