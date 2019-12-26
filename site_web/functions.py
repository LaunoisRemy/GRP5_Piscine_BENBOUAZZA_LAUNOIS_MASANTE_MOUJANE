from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import *
from .forms import *


"""
Fonction qui permet de récuperer la liste des bonne réponses grace a un idToeic
"""
def getBonneReponse(id_TOEIC) :

    question = list(Question.objects.filter( id_TOEIC=id_TOEIC))
    listeBonneReponse = ([],[])
    for q in question :
        id_SousPartie = q.id_SousPartie.id
        #Ajout selon le type  de partie
        if(id_SousPartie==1):
            listeBonneReponse[0].append(q.reponse_Juste)
        elif(id_SousPartie==2):
            listeBonneReponse[1].append(q.reponse_Juste)
    return(listeBonneReponse)


"""
Fonction qui compare deux listes de caractères entre elles 
Renvoie un int, le score résultant de la comparaison
"""
def comparaisonReponse(bonneReponses,userReponses):    
    score = [0,0]
    for ssPartie in range(0,2):

        i=0
        liste_Bonne_Reponse_Sous_Partie = bonneReponses[ssPartie]
        liste_Reponse_Sous_Partie = userReponses[ssPartie]

        while i<len(liste_Bonne_Reponse_Sous_Partie):
            if(liste_Reponse_Sous_Partie[i] is not None):
                if liste_Reponse_Sous_Partie[i].lower()==liste_Bonne_Reponse_Sous_Partie[i].lower():
                    score[ssPartie]=score[ssPartie]+1
            i+=1
    return(score)