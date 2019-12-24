from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db.models import Sum,Avg,FloatField
from django.db.models.functions import Exp
from .fonctions_TOEIC import NOTE_L,NOTE_R
from django.db.models.functions import Cast


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

    

    ### scoretot recupère le nombre de bonne réponses par toeic passé et par partie de l'élève qui a pour id id_eleve
    scoretot = ScoreParPartie.objects.filter( # Query set
        id_Eleve=id_eleve).values('id_TOEIC','id_SousPartie__type_Partie').annotate(
        score=Sum('score')).values('id_TOEIC','id_Eleve__nom','id_SousPartie__type_Partie','score')


    ListeNoteParPartie = list(scoretot) # Transformation de la query set en list

    ##Ici on fait la liste qui contient les notes par partie
    for i in ListeNoteParPartie : 
        if i["id_SousPartie__type_Partie"]=="L":
            i["score"]=(NOTE_L(i["score"])) # Recuperation du score d'un dictionnaire et changement du score grace a la fonction de calcul
        else:
            i["score"]=(NOTE_R(i["score"]))

    listeR=[]
    listeL=[]
    listeTOT=[]
    Tout=[]

    #On créer la liste des notes Listening

    for i in ListeNoteParPartie : 
        if i["id_SousPartie__type_Partie"]=="L":
            listeL.append(i)

    #On créer la liste des notes Reading

    for i in ListeNoteParPartie : 
        if i["id_SousPartie__type_Partie"]=="R":
            listeR.append(i)

    #Oncréer la liste des notes Total

    for i in range(len(listeR)):
        scoretot=listeR[i]["score"]+listeL[i]["score"]
        nouveauquery= {'id_TOEIC': listeR[i]["id_TOEIC"], 'id_Eleve__nom': listeR[i]["id_Eleve__nom"], 'id_SousPartie__type_Partie': 'TOT', 'score': scoretot}
        listeTOT.append(nouveauquery)

    for i in range(len(listeR)):
        Tout.append(listeR[i])
        Tout.append(listeL[i])
        Tout.append(listeTOT[i])

    
    
    #scoretot=query(ListeNoteParPartie)
    
    #Pour afficher les toeic, je pense qu'il faudrait créer un model qui recupère les notes calculées pour ne pas avoir à les recalculer à chaque fois
    #qu'on veut les afficher.

    #scoretot=scoretot.objects.values('id_TOEIC').annotate(score=Sum('score')).values('id_Toeic','id_Eleve__nom','id_SousPartie__type_Partie','score')
    return liste(request,"Derniers résultats :",Tout)


    ### C'est ici que le professeur peut voir les statistiques sur les résultats de toeic
def espace_professeur(request):
    scoretot=ScoreParPartie.objects.values('id_TOEIC','id_SousPartie__type_Partie').annotate(
        score_type=Sum('score')).values('id_TOEIC','id_Eleve__nom','id_SousPartie__type_Partie','score_type')
    return liste(request,"Voici tout les résultats :",scoretot)
    