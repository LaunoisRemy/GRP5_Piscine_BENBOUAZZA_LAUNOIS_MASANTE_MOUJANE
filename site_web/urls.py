from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('home', views.home),
    path('session', views.session),
    path('eleve/liste', views.liste_Eleve),
    path('classe/liste', views.liste_Classe),
]
