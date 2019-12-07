from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db.models import Sum
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

    #scoretot = ScoreParPartie.objects.filter(id_Eleve=id_eleve).values('id_SousPartie__type_Partie').annotate('id_TOEIC').annotate(Sum('score'))

    ### Ici scoretot est le tableau, des des scores par parties et par toeic de l'élève qui a pour id id_eleve
    #scoretot = ScoreParPartie.objects.filter(id_Eleve=id_eleve).values('id_TOEIC','id_SousPartie__type_Partie','score')

    ### scoretot recupère ls notes par toeic et par partir de l'élève qui a pour id id_eleve
    scoretot = ScoreParPartie.objects.filter(id_Eleve=id_eleve).values('id_TOEIC','id_SousPartie__type_Partie').annotate(score_type=Sum('score')).values('id_TOEIC','id_SousPartie__type_Partie','score_type')

    #.values('lib_Partie').annotate(Sum('score')
    return liste(request,"Derniers résultats :",scoretot)

    #print(scoretot)
    
    #sum = 0
    #for j in score:
    #    sum = sum + j.score 
    #return HttpResponse(sum)

    ### La partie en commentaire était une tentative pour récupérer la somme des points par parties mais 
    ### Il est surement plus simple de faire des requêtes sur la base de donnée