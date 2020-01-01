from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db.models import Sum,Avg,FloatField,Count
from django.db.models.functions import Exp
from .fonctions_TOEIC import NOTE_L,NOTE_R
from django.db.models.functions import Cast
from django.views.generic import TemplateView

from .filters import SearchFilter,FiltreNoteParPartie
from django.contrib.auth.models import User

from chartit import DataPool, Chart

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

    test = ScoreParPartie.objects.filter(id_Eleve=id_eleve)
    print(test)

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

    #TODO il faudrait aussi afficher si le toeic est réussi ou non
    
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
    

        

    ### Vue dans laquelle on va utiliser le filtre SearchFilter
def search(request):
    user_list = ScoreParPartie.objects.all()
    user_filter = SearchFilter(request.GET, queryset=user_list)
    return render(request, 'espace_prof/search_user.html', {'filter': user_filter})

def filtre_note_par_partie(request):
    user_list = ScoreParPartie.objects.all()#.values('id_TOEIC','id_SousPartie__type_Partie').annotate(score=Sum('score')).values('id_TOEIC','score','id_SousPartie__lib_Partie','id_Eleve__nom',)
    ### PROBLEME : Calcul bien la somme des bonne réponse par partie mais problème d'affichage
    print(user_list)
    user_filter = FiltreNoteParPartie(request.GET, queryset=user_list) #Récup
    #user_filter n'est pas un queryset, user_filter.qd l'est !
    print("Le filtre récupéré",user_filter.qs)
    







    return render(request, 'espace_prof/search_user.html', {'filter': user_filter})

def graph1(request,user_filter):
    search1 =  DataPool(
        series=
        [{'options': {
            'source': user_filter.qs.filter(id_SousPartie__type_Partie='1')},
            'terms': ['score','id_TOEIC']}
            ])
    cht1 = Chart(
        datasource = search1,            
        series_options = 
        [{'options':{'type':'column','stacking':False},
        'terms':{                    
            'score': [
                'id_TOEIC']
                    }}] 
                    )


    
    return render(request,'espace_prof/graphes.html',{'cht1':cht1})

### Comment afficher le graph en plus du resultat de la recherche

###Création des graphes

def graphview(request):

   #requete = ScoreParPartie.objects.all()
   # for i in range(0,11):
     #   requete = requete.annotate(score=i).aggregate(occ=Count('score'))

    fieldname = 'score'
    requete1 = ScoreParPartie.objects.filter(id_SousPartie__lib_Partie=1).values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    requete2 = ScoreParPartie.objects.filter(id_SousPartie__lib_Partie=2).values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    requete3 = ScoreParPartie.objects.filter(id_SousPartie__lib_Partie=3).values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    requete4 = ScoreParPartie.objects.filter(id_SousPartie__lib_Partie=4).values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    requete5 = ScoreParPartie.objects.filter(id_SousPartie__lib_Partie=5).values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    requete6 = ScoreParPartie.objects.filter(id_SousPartie__lib_Partie=6).values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    requete7 = ScoreParPartie.objects.filter(id_SousPartie__lib_Partie=7).values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    requete8 = ScoreParPartie.objects.filter(id_SousPartie__lib_Partie=8).values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    requeteR = ScoreParPartie.objects.filter(id_SousPartie__type_Partie='R').values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    requeteL = ScoreParPartie.objects.filter(id_SousPartie__type_Partie='L').values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    print('requeteR :',requeteR)


    # Graph partie 1

    search1 =  DataPool(
        series=
        [{'options': {
            'source': requete1},
            'terms': ['the_count','score']}
            ])
    cht1 = Chart(
        datasource = search1,            
        series_options = 
        [{'options':{'type':'column','stacking':False},
        'terms':{                    
            'score': [
                'the_count']
                    }}] ,
                    
        chart_options = {'yAxis':{'allowDecimals':False,'tickInterval':1},
        'xAxis': {'tickInterval':1}}
    )
    ## Graph partie 2
    search2 =  DataPool(
        series=
        [{'options': {
            'source': requete2},
            'terms': ['the_count','score']}
            ])
    cht2 = Chart(
        datasource = search2,            
        series_options = 
        [{'options':{'type':'column','stacking':False},
        'terms':{                    
            'score': [
                'the_count']
                    }}] ,
        chart_options = {'yAxis':{'allowDecimals':False,'tickInterval':1},
        'xAxis': {'tickInterval':1}}
                    )

    ## Graph partie 3
    search3 =  DataPool(
        series=
        [{'options': {
            'source': requete3},
            'terms': ['the_count','score']}
            ])
    cht3 = Chart(
        datasource = search3,            
        series_options = 
        [{'options':{'type':'column','stacking':False},
        'terms':{                    
            'score': [
                'the_count']
                    }}] 
                    )
    ## Graph partie 4
    search4 =  DataPool(
        series=
        [{'options': {
            'source': requete4},
            'terms': ['the_count','score']}
            ])
    cht4 = Chart(
        datasource = search4,            
        series_options = 
        [{'options':{'type':'column','stacking':False},
        'terms':{                    
            'score': [
                'the_count']
                    }}] ,

         chart_options = {'yAxis':{'allowDecimals':False,'tickInterval':1},
        'xAxis': {'tickInterval':1}}
                    )

    ## Graph partie R

    searchR =  DataPool(
        series=
        [{'options': {
            'source': requeteR},
            'terms': ['the_count','score']}
            ])
    chtR = Chart(
        datasource = searchR,            
        series_options = 
        [{'options':{'type':'column','stacking':False},
        'terms':{                    
            'score': [
                'the_count']
                    }}] ,

         chart_options = {'yAxis':{'allowDecimals':False,'tickInterval':1},
        'xAxis': {'tickInterval':1}}
                    )
    ## Graph partie L
    searchL =  DataPool(
        series=
        [{'options': {
            'source': requeteL},
            'terms': ['the_count','score']}
            ])
    chtL = Chart(
        datasource = searchL,            
        series_options = 
        [{'options':{'type':'column','stacking':False},
        'terms':{                    
            'score': [
                'the_count']
                    }}] ,

         chart_options = {'yAxis':{'allowDecimals':False,'tickInterval':1},
        'xAxis': {'tickInterval':1},
        'min': 0,'max':10}
                    )

    

    return render(request,'espace_prof/graphes.html',{'chart_list':[cht1,cht2,cht3,cht4,chtL,chtR]})