from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home),
    path('session', views.session),
    path('eleve/liste', views.liste_Eleve),
    path('classe/liste', views.liste_Classe),
    path('espace_eleve/<int:id_eleve>', views.espace_eleve), # Ici le <int:id_eleve capture l'id de l'élève, et on en a besoin pour savoir les résultats de qui on veut afficher
    # Exemple de chemin pour l'espace élève http://localhost:8000/espace_eleve/1 Por accéder aux résultats de l'élève qui a pour clé primaire 1
    # Le but ensuite est que une fois que l'utilisateur se connecte on récupère sa clé primaire et on lui affiche ses resultats
    path('espace_professeur', views.espace_professeur),
    path('espace_prof', views.search),
    path('filtre_notepp',views.filtre_note_par_partie)
]
