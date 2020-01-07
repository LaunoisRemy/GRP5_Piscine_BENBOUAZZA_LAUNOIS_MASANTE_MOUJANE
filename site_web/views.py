from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import *
from django.db.models import Sum,Avg,FloatField
from django.db.models.functions import Exp,Cast
from .fonctions_TOEIC import NOTE_L,NOTE_R
from .forms import *
from .functions import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

import datetime

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


# TODO deux fonctions qui font presque la même chose, synthétiser 
"""
Fonction qui permet de réaliser la vue lors d'un passage de TOEIC
"""
def repondTOEIC(request,id_Toeic):
    template_name ='toeic.html' #Nom de la page

  
    listeBonneReponse = getBonneReponse(id_Toeic)
    nbRepReading = len(listeBonneReponse[0])
    nbRepListening = nbRepReading+ len(listeBonneReponse[1])
    if len(listeBonneReponse) == 0 :
        raise Http404

    if request.method == 'GET': #Pour récupérer la page
        formset = qcmFormSet(prefix=' Question ')  
    elif request.method == 'POST':

        userReponses=([],[])
        formset = qcmFormSet(request.POST,prefix=' Question ')

        compteurReponse=0

        if formset.is_valid():#Action de sécurité
            for form in formset: #On récupère chacune des réponses 
                question  = form.cleaned_data.get('question')
                if(compteurReponse<nbRepReading):
                    userReponses[0].append(question) #On met chacune des réponses dans une liste
                elif(compteurReponse>=nbRepReading and compteurReponse < nbRepListening ):
                    userReponses[1].append(question) #On met chacune des réponses dans une liste
                compteurReponse+=1

           
        score = comparaisonReponse(listeBonneReponse,userReponses)
        # Recupération de l'élève, provisoire
        # TODO Quand les comptes seront fait récupérer par rapport au compte
        eleve = Eleve.objects.all()[0]
        print (eleve)
        # Sauvegarde du score
        
        for ssPartie in range(0,2):
            #Score a sauvegarder
            data = {
                'id_Eleve' : eleve.id,
                'id_TOEIC' : id_Toeic,
                'id_SousPartie' : ssPartie+1,
                'score' : score[ssPartie],
                'date_Passage' : datetime.datetime.now()
            }
            
            scorePartie = ScoreParPartieForm(data)
            if(scorePartie.is_valid()):
                scorePartie.save()
                print("yes") 
            else:
                print("no")

        print(listeBonneReponse)
        print(userReponses)   
        print(score)
        return redirect(home)

    return render(request, template_name, {'formset':formset })


def creerTOEIC(request,nomToeic):
    template_name ='toeic.html' #Nom de la page
    if request.method == 'GET': #Pour récupérer la page
        formset = qcmFormSet(prefix=' Question ')
    elif request.method == 'POST':

        userReponses=[]
        formset = qcmFormSet(request.POST,prefix=' Question ')
        if formset.is_valid():#Action de sécurité

            toeic = ToeicForm({'lib_TOEIC': nomToeic})
            toeic.save()
            question = list(TOEIC.objects.filter( lib_TOEIC=nomToeic))
            idToeic = question[len(question)-1].id
            i=0        
            for form in formset: #On récupère chacune des réponses 
                reponse  = form.cleaned_data.get('question')
                if(i<2):
                    data = {
                        'id_Question' : i,
                        'id_TOEIC' : idToeic,
                        'id_SousPartie' : 1,
                        'reponse_Juste' : reponse
                    }
                else:
                    data = {
                        'id_Question' : i,
                        'id_TOEIC' : idToeic,
                        'id_SousPartie' : 2,
                        'reponse_Juste' : reponse
                    }
                questionForm = QuestionForm(data)
                questionForm.save()
                i+=1
                userReponses.append(question) #On met chacune des réponses dans une liste
        return redirect(home)
    return render(request, template_name, {'formset':formset })

def liste(request,nom,querryset):  
    context ={
        "titre":nom,
        "liste":querryset
    }
    return render(request,"liste.html",context)  

def liste_Eleve(request):
    return liste(request,"Eleves",Eleve.objects.all())  
def liste_Classe(request):
    return liste(request,"Classes",Classe.objects.all())  

def liste_TOEIC(request):
    listToeic =  ( Question.objects.all().values('id_TOEIC').distinct() ) 
    toeic = TOEIC.objects.filter(id__in=listToeic)
    if request.method == 'GET': #Pour récupérer la page
        test = NomToeicForm(None)
        context ={
            "titre":"Liste de Toeic",
            "liste":toeic,
            "test" : test
        }
        return render(request,"listeToeic.html",context) 
    elif request.method == 'POST':
        form = NomToeicForm(request.POST)

        if(form.is_valid()):
            nom=form.cleaned_data.get('nom')
            return redirect(creerTOEIC,nom)
        return redirect(liste_TOEIC)
 



def liste_groupe(request):
    return liste(request,"Groupes",Groupe.objects.all())

def session(request):    
    context ={
        "titre":"Session"
    }
    return render(request,"liste.html",context)

def espace_eleve(request, id_eleve): # Quand la fonction est appelée elle a pris en paramètre un id_eleve et affiche les résultats aux toeic de l'élève concerné

    #scoretot = ScoreParPartie.objects.filter(id_Eleve=id_eleve).values('id_SousPartie__type_Partie').annotate('id_TOEIC').annotate(Sum('score'))

    ### Ici scoretot est le tableau, des des scores par parties et par toeic de l'élève qui a pour id id_eleve
    #scoretot = ScoreParPartie.objects.filter(id_Eleve=id_eleve).values('id_TOEIC','id_SousPartie__type_Partie','score')

    

    ### scoretot recupère le nombre de bonne réponses par toeic passé et par partie de l'élève qui a pour id id_eleve
    scoretot = ScoreParPartie.objects.filter( # Query set
        id_Eleve=id_eleve).values('id_TOEIC','id_SousPartie__type_Partie').annotate(
        score=Sum('score')).values('id_TOEIC','id_Eleve__nom','id_SousPartie__type_Partie','score')


    listTest = list(scoretot) # Transformation de la query set en list
    for i in listTest : 
        if i["id_SousPartie__type_Partie"]=="L":
            i["score"]=(NOTE_L(i["score"])) # Recuperation du score d'un dictionnaire et changement du score grace a la fonction de calcul
        else:
            i["score"]=(NOTE_R(i["score"]))
    
    #Pour afficher les toeic, je pense qu'il faudrait créer un model qui recupère les notes calculées pour ne pas avoir à les recalculer à chaque fois
    #qu'on veut les afficher.

    return liste(request,"Derniers résultats :",listTest)

    
    #print(scoretot)

    ### C'est ici que le professeur peut voir les statistiques sur les résultats de toeic
def espace_professeur(request):
    scoretot=ScoreParPartie.objects.values('id_TOEIC','id_SousPartie__type_Partie').annotate(
        score_type=Sum('score')).values('id_TOEIC','id_Eleve__nom','id_SousPartie__type_Partie','score_type')
    return liste(request,"Voici tout les résultats :",scoretot)


def register(request):

    if request.method == 'GET':
        form = UserForm()
        formUser = UserCreationForm()
        context = { 'form' : form , 'formUser' : formUser}
        return render(request,'registration/register.html', context)
    elif request.method == 'POST':

        form = UserForm(request.POST)
        formUser = UserCreationForm(request.POST)
        if form.is_valid() and formUser.is_valid():
            user = formUser.save()

            """# TODO cleaned data
            username = formUser.cleaned_date['username']
            password = formUser.cleaned_data['paswword1']
            user = authenticate(username=username, password=password)
            login(request, user)
            """
        

            post = form.save(commit=False)
            post.user = user
            post.save()
            return redirect(home)
        else :
            return redirect('espace_professeur')


