from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import *
from .forms import *


"""
Fonction qui permet de récuperer la liste des bonne réponses grace a un idToeic
"""
def getBonneReponse(id_TOEIC) :

    question = list(Question.objects.filter( id_TOEIC=id_TOEIC))
    listeBonneReponse = ([],[],[],[],[],[],[])
    for q in question :
        id_SousPartie = q.id_SousPartie.id
        listeBonneReponse[id_SousPartie-1].append(q.reponse_Juste)
        #Ajout selon le type  de partie
    return(listeBonneReponse)


"""
Fonction qui compare deux listes de caractères entre elles 
Renvoie un int, le score résultant de la comparaison
"""
def comparaisonReponse(bonneReponses,userReponses):    
    score = [0,0,0,0,0,0,0]
    for ssPartie in range(0,7):

        i=0
        liste_Bonne_Reponse_Sous_Partie = bonneReponses[ssPartie]
        liste_Reponse_Sous_Partie = userReponses[ssPartie]

        while i<len(liste_Bonne_Reponse_Sous_Partie):
            if(liste_Reponse_Sous_Partie[i] is not None):
                if liste_Reponse_Sous_Partie[i].lower()==liste_Bonne_Reponse_Sous_Partie[i].lower():
                    score[ssPartie]=score[ssPartie]+1
            i+=1
    return(score)
    
def compteurBonneRep(formset):
    userReponses=([],[],[],[],[],[],[])
    compteurReponse = 1
    for form in formset:  # On récupère chacune des réponses
        question = form.cleaned_data.get('question')
        if(compteurReponse <= 6):
            # On met chacune des réponses dans une liste
            userReponses[0].append(question)
        elif(compteurReponse >= 7 and compteurReponse <= 31):
            # On met chacune des réponses dans une liste
            userReponses[1].append(question)
        elif(compteurReponse >= 32 and compteurReponse <= 70):
            userReponses[2].append(question)
        elif(compteurReponse >= 71 and compteurReponse <= 100):
            userReponses[3].append(question)
        elif(compteurReponse >= 101 and compteurReponse <= 130):
            userReponses[4].append(question)
        elif(compteurReponse >= 131 and compteurReponse <= 146):
            userReponses[5].append(question)
        elif(compteurReponse >= 147 and compteurReponse <= 200):
            userReponses[6].append(question)
        compteurReponse += 1
    return userReponses