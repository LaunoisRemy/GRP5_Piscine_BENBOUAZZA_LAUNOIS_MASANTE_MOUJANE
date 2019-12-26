from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import *
from .forms import *
from .functions import *


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
    listeBonneReponse = getBonneReponse(id_Toeic)
    nbRepReading = len(listeBonneReponse[0])
    nbRepListening = nbRepReading+ len(listeBonneReponse[1])
    

    if len(listeBonneReponse) == 0 :
        raise Http404

    template_name ='toeic.html' #Nom de la page
    if request.method == 'GET': #Pour récupérer la page
        formset = qcmFormSet(request.GET or None)
    elif request.method == 'POST':
        userReponses=([],[])
        compteurReponse=0
        formset = qcmFormSet(request.POST)

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
            
            data = {
                'id_Eleve' : eleve.id,
                'id_TOEIC' : id_Toeic,
                'id_SousPartie' : ssPartie+1,
                'score' : score[ssPartie]

            }
            
            scorePartie = ScoreParPartieForm(data)
            if(scorePartie.is_valid()):
                scorePartie.save()
                print("yes") 

        print(listeBonneReponse)
        print(userReponses)   
        print(score)
        return redirect(home)

    return render(request, template_name, {'formset':formset })


def creerTOEIC(request):
    template_name ='toeic.html' #Nom de la page
    if request.method == 'GET': #Pour récupérer la page
        formset = qcmFormSet(request.GET or None)
    elif request.method == 'POST':
        userReponses=[]
        formset = qcmFormSet(request.POST)
        if formset.is_valid():#Action de sécurité
            toeic = ToeicForm({'lib_TOEIC': "test"})
            toeic.save()
            question = list(TOEIC.objects.filter( lib_TOEIC="test"))
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
                    questionForm = QuestionForm(data)
                    questionForm.save()
                i+=1
                userReponses.append(question) #On met chacune des réponses dans une liste
        return redirect(home)
    return render(request, template_name, {'formset':formset })

def liste(request,nom,querryset,url):  
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
    # TODO afficher seulement les toeics avec des réponses
    listToeic =  ( Question.objects.all().values('id_TOEIC').distinct() ) 
    toeic = TOEIC.objects.filter(id__in=listToeic)
    print(toeic)
 

    context ={
        "titre":"Liste de Toeic",
        "liste":toeic
    }
    return render(request,"liste.html",context) 
def liste_groupe(request):
    return lsite(request,"Groupes",Groupe.objects.all())

def session(request):    
    context ={
        "titre":"Session"
    }
    return render(request,"index.html",context)