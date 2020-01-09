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

import json
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


    ### scoretot recupère le nombre de bonne réponses par toeic passé et par partie de l'élève qui a pour id id_eleve
    scoretot = ScoreParPartie.objects.filter( # Query set
        id_Eleve=id_eleve).values('id_TOEIC','id_SousPartie__type_Partie').annotate(
        score=Sum('score')).values('id_TOEIC','id_Eleve__nom','id_Eleve__prenom','id_SousPartie__type_Partie','score','id_TOEIC__lib_TOEIC')
        ## TODO Nom et prenom pas besoin car on peut les récupérer directement et ne pas les trainer dans le queryset

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
    print('tTTTTTTTOUUOTUTTUTTUO()',Tout)

    #TODO il faudrait aussi afficher si le toeic est réussi ou non
    #context = {"reading":listeR,"listening":listeL,"total":listeTOT}
    context = {'resultats':Tout,'nom':Tout[0]['id_Eleve__nom'],'prenom':Tout[0]['id_Eleve__prenom']}
    print('CONNNNNNTEXTXTTTXXTT',context)
    #scoretot=scoretot.objects.values('id_TOEIC').annotate(score=Sum('score')).values('id_Toeic','id_Eleve__nom','id_SousPartie__type_Partie','score')
    return render(request,"espace_eleve/notes_toeic.html",context) # TODO changer l'affichage des notes pour avoir un truc plus propre
    


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
    #print(user_list)
    user_filter = FiltreNoteParPartie(request.GET, queryset=user_list) #Récup
    #user_filter n'est pas un queryset, user_filter.qs l'est !
    #print("Le filtre récupéré",user_filter.qs)
    
    fieldname = 'score'
    requete1 = user_filter.qs.filter(id_SousPartie__lib_Partie=1).values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    requete2 = user_filter.qs.filter(id_SousPartie__lib_Partie=2).values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    requete3 = user_filter.qs.filter(id_SousPartie__lib_Partie=3).values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    requete4 = user_filter.qs.filter(id_SousPartie__lib_Partie=4).values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    requete5 = user_filter.qs.filter(id_SousPartie__lib_Partie=5).values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    requete6 = user_filter.qs.filter(id_SousPartie__lib_Partie=6).values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    requete7 = user_filter.qs.filter(id_SousPartie__lib_Partie=7).values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    requete8 = user_filter.qs.filter(id_SousPartie__lib_Partie=8).values(fieldname).order_by(fieldname).annotate(the_count=Count(fieldname))
    requeteR = user_filter.qs.filter(id_SousPartie__type_Partie='R').values('id_TOEIC','id_Eleve').order_by('id_TOEIC','id_Eleve').annotate(sommetot=Sum('score'))
    requeteL = user_filter.qs.filter(id_SousPartie__type_Partie='L').values('id_TOEIC','id_Eleve').order_by('id_TOEIC','id_Eleve').annotate(sommetot=Sum('score'))
    print(requeteR)
  

    # On exprime transmet les données des queryset en liste pour être plus maniable, avec chartit problèmes pour les notes etc
    # du coup j'ai changé et utilisé highchart qui utilise les listes.
    # Certes moins efficace mais beaucoup plus maniable


    score1 = [0,0,0,0,0,0,0]
    cat1 = ["0","1","2","3","4","5","6"]
    for j in requete1:
        score1[j['score']]+=j['the_count']
    score1 = json.dumps(score1)
    cat1 = json.dumps(cat1)
    
    score2=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    cat2 = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25"]
    for j in requete2:
        score2[j['score']]+=j['the_count']
    
    score2 = json.dumps(score2)
    cat2 = json.dumps(cat2)

    score3=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    cat3 = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39"]
    for j in requete3:
        score3[j['score']]+=j['the_count']
    
    score3 = json.dumps(score3)
    cat3 = json.dumps(cat3)

    score4=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    cat4 = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"]
    for j in requete4:
        score4[j['score']]+=j['the_count']
    
    score4 = json.dumps(score4)
    cat4 = json.dumps(cat4)

    score5=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    cat5 = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"]
    for j in requete5:
        score5[j['score']]+=j['the_count']
    
    score5 = json.dumps(score5)
    cat5 = json.dumps(cat5)

    score6 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    cat6 = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"]
    for j in requete6:
        score6[j['score']]+=j['the_count']
    score6 = json.dumps(score6)
    cat6 = json.dumps(cat6)
    
    score7=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    cat7 = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54"]
    for j in requete7:
        score7[j['score']]+=j['the_count']
    
    score7 = json.dumps(score7)
    cat7 = json.dumps(cat7)
    
    scoreR=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    catR = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100"]
    for j in requeteR:
        scoreR[j['sommetot']]+=1
    
    scoreR = json.dumps(scoreR)
    catR = json.dumps(catR)
    
    scoreL=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    catL = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100"]
    for j in requeteL:
        scoreL[j['sommetot']]+=1
    
    scoreL = json.dumps(scoreL)
    catL = json.dumps(catL)

    return render(request,'espace_prof/search_user.html',{'cat1':cat1,'score1':score1,'cat2':cat2,'score2':score2,'cat3':cat3,'score3':score3,'cat4':cat4,'score4':score4,'cat5':cat5,'score5':score5,'cat6':cat6,'score6':score6,'cat7':cat7,'score7':score7,'catR':catR,'scoreR':scoreR,'catL':catL,'scoreL':scoreL,'filter': user_filter})


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

