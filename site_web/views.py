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
def repondTOEIC(request):
    context ={
        "titre":"ReponseToeic"
    }
    return render(request,"toeic.html",context)
"""
def repondTOEIC(request):
    template_name ='toeic.html'
    if request.method == 'GET':
        formset = qcmFormSet(request.GET or None)
    elif request.method == 'POST':
        formset = qcmFormSet(request.POST)
        if formset.is_valid():
            for form in formset: 
                picked  = form.cleaned_data.get('picked')
                print(picked)
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