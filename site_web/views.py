from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import *
from .forms import *



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

"""
Fonction qui permet de récuperer la liste des bonne réponses grace a un idToeic
"""
def getBonneReponse(id_Toeic) :
    question = list(Question.objects.filter( id_TOEIC=id_Toeic))
    listeBonneReponse = []
    for q in question :
        listeBonneReponse.append(q.reponse_Juste)
    return(listeBonneReponse)
"""
Fonction qui compare deux listes de caractères entre elles 
Renvoie un int, le score résultant de la comparaison
"""
def comparaisonReponse(bonneReponses,userReponses):
        score=0
        i=0
        while i<len(bonneReponses):
            if(userReponses[i] is not None):
                if userReponses[i].lower()==bonneReponses[i].lower():
                    score+=1
            i+=1
        return(score)
"""
Fonction qui permet de réaliser la vue lors d'un passage de TOEIC
"""
def repondTOEIC(request,id_Toeic):
    listeBonneReponse = getBonneReponse(id_Toeic)
    print(type(listeBonneReponse))
    if len(listeBonneReponse) == 0 :
        raise Http404

    template_name ='toeic.html' #Nom de la page
    if request.method == 'GET': #Pour récupérer la page
        formset = qcmFormSet(request.GET or None)
    elif request.method == 'POST':
        userReponses=[]
        formset = qcmFormSet(request.POST)
        if formset.is_valid():#Action de sécurité
            for form in formset: #On récupère chacune des réponses 
                question  = form.cleaned_data.get('question')
                userReponses.append(question) #On met chacune des réponses dans une liste
        score = comparaisonReponse(listeBonneReponse,userReponses)
        return redirect(home)

    return render(request, template_name, {'formset':formset })


def repondTOEIC(request):
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
        #return redirect(home)
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
 
    context ={
        "titre":"Liste de Toeic",
        "liste":TOEIC.objects.all()
    }
    return render(request,"liste.html",context) 
def liste_groupe(request):
    return lsite(request,"Groupes",Groupe.objects.all())

def session(request):    
    context ={
        "titre":"Session"
    }
    return render(request,"index.html",context)