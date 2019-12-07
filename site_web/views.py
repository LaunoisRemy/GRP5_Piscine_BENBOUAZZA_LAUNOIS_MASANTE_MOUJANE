from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import qcm



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
    if request.method == 'POST':
        form = qcm(request.POST)
        if form.is_valid():
            picked  = form.cleaned_data.get('picked')
            print(picked)
    else:
        form = qcm

    return render(request,'toeic.html', {'form':form })

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