from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        context ={
        "titre":"Bonjour " + request.user.username
        }
    else :
        context ={
        "titre":"Home"
        }
    return render(request,"index.html",context)


def liste(request,nom,querryset):  
    context ={
        "titre":nom,
        "liste":querryset
    }
    return render(request,"index.html",context)  
def liste_Eleve(request):
    return liste(request,"Eleves",Eleve.objects.all())  
def liste_Classe(request):
    return liste(request,"Classes",Classe.objects.all())  
def liste_TOEIC(request):
    return liste(request,"libelleTOEIC",TOEIC.objects.all()) 
def liste_groupe(request):
    return liste(request,"Groupes",Groupe.objects.all())

def session(request):    
    context ={
        "titre":"Session"
    }
    return render(request,"index.html",context)

def espace_eleve(request, id_eleve): # Quand la fonction est appelée elle a pris en paramètre un id_eleve et affiche les résultats aux toeic de l'élève concerné
    score = ScoreParPartie.objects.filter(id_Eleve=id_eleve)
    return liste(request,"Derniers résultats :",score)
    
    #sum = 0
    #for j in score:
    #    sum = sum + j.score 
    #return HttpResponse(sum)

    ### La partie en commentaire était une tentative pour récupérer la somme des points par parties mais 
    ### Il est surement plus simple de faire des requêtes sur la base de donnée