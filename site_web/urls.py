from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('home', views.home, name='index'),
    path('session', views.session),
    path('eleve/liste', views.liste_Eleve),
    path('classe/liste', views.liste_Classe),
    path('espace_eleve', views.espace_eleve,name="stats_Eleve"), # Ici le <int:id_eleve capture l'id de l'élève, et on en a besoin pour savoir les résultats de qui on veut afficher
    # Exemple de chemin pour l'espace élève http://localhost:8000/espace_eleve/1 Por accéder aux résultats de l'élève qui a pour clé primaire 1
    # Le but ensuite est que une fois que l'utilisateur se connecte on récupère sa clé primaire et on lui affiche ses resultats
    path('espace_professeur', views.espace_professeur, name ="espace_professeur",),
    path('liste_TOEIC', views.liste_TOEIC, name="liste_TOEIC"),
    path('creerTOEIC/<str:nomToeic>',views.creerTOEIC),
    path('repondTOEIC/<int:id_TEnCours>',views.repondTOEIC, name="repondTOEIC"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.register, name="register" ),
    path('espace_prof', views.search),
    path('filtre_notepp',views.filtre_note_par_partie,name="stats_Prof"),
]
