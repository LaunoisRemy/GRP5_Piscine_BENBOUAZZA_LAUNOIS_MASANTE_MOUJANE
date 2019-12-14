from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import qcm, qcmFormSet



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
            if userReponses[i].lower()==bonneReponses[i].lower():
                score+=1
            i+=1
        return(score)
"""
Fonction qui permet de réaliser la vue lors d'un passage de TOEIC
"""
def repondTOEIC(request,id_Toeic):
    
    listeBonneReponse = getBonneReponse(id_Toeic)

    template_name ='toeic.html' #Nom de la page
    if request.method == 'GET': #Pour récupérer la page
        formset = qcmFormSet(request.GET or None)
    elif request.method == 'POST':
        userReponses=[]
        formset = qcmFormSet(request.POST)
        if formset.is_valid():#Action de sécurité
            for form in formset: #On récupère chacune des réponses 
                picked  = form.cleaned_data.get('picked')
                userReponses.append(picked) #On met chacune des réponses dans une liste
        print(userReponses)
        print(listeBonneReponse)
    score = comparaisonReponse(listeBonneReponse,userReponses)
    print(score)

    return render(request, template_name, {'formset':formset })

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
    return lsite(request,"Groupes",Groupe.objects.all())

def session(request):    
    context ={
        "titre":"Session"
    }
    return render(request,"index.html",context)