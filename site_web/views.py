from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import *
from django.db.models.functions import Exp,Cast
from .fonctions_TOEIC import NOTE_L,NOTE_R
from .forms import *
from .functions import *
from django.contrib.auth import authenticate, login
from django.db.models import Sum,Avg,FloatField,Count
from .fonctions_TOEIC import NOTE_L,NOTE_R
from django.views.generic import TemplateView
from .filters import SearchFilter,FiltreNoteParPartie
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.contrib.auth.base_user import BaseUserManager
import statistics
import json
import os
# Create your views here.


def mediane(score,effectiftot):
        mediane1=0
        k=0
        while (mediane1<effectiftot/2) :
            mediane1+=score[k]
            k+=1
        return k-1

def home(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(filtre_note_par_partie)
        else :
            return redirect(espace_eleve)
    else :
        return redirect('login')

"""
Fonction qui permet de réaliser la vue lors d'un passage de TOEIC
"""
def repondTOEIC(request,id_TEnCours):
    ToeicCourant = TOEICEnCours.objects.filter(id=id_TEnCours)[0]
    #print(ToeicCourant)
    id_Toeic = ToeicCourant.id_TOEIC.id
    #print(id_Toeic)
 

    if(request.user.is_superuser):
        return redirect(home)
    else :
        template_name ='toeic.html' #Nom de la page
        listeBonneReponse = getBonneReponse(id_Toeic)
        if len(listeBonneReponse) == 0 :
            raise Http404
        if request.method == 'GET': #Pour récupérer la page
            formset = qcmEleveFormSet(prefix=' Question ')  
        elif request.method == 'POST':

            formset = qcmFormSet(request.POST or None,prefix=' Question ')
            listesReponsesUser = []
            for form in formset :
                if(form.is_valid()):
                    question = form.cleaned_data.get('question')
                    listesReponsesUser.append(question)
                else :
                    listesReponsesUser.append(None)

            userReponses = compteurBonneRep(listesReponsesUser)

            #print(userReponses)   
            score = comparaisonReponse(listeBonneReponse,userReponses)
            # Recupération de l'élève, provisoire
            #eleve = Eleve.objects.all()[0]
            utilisateur = request.user
            eleve = Eleve.objects.filter(user=utilisateur)[0]
            # Sauvegarde du score

            datepassage=datetime.now()
            # AJouté par Ayoub, pour qu'on ait pas des temps de passages différents pour des parties dans un même suejt
            # On prend une date unique
            for ssPartie in range(1,len(score)+1):
                #print(eleve.id)
                #print(ToeicCourant)
                #print(ssPartie)
                #print(score[ssPartie-1])
                #print(datepassage)

                #Score a sauvegarder
                data = {
                    'id_Eleve' : eleve.id,
                    'id_TOEICEnCours' : ToeicCourant.id,
                    'id_SousPartie' : ssPartie,
                    'score' : score[ssPartie-1],
                    'date_Passage' : datepassage
                }
                
                scorePartie = ScoreParPartieForm(data)
                #print(scorePartie.is_valid())
                #print(scorePartie.errors)

                if(scorePartie.is_valid()):
                    scorePartie.save()
        

            #print(listeBonneReponse)
            #print(userReponses)   
            #print(score)
            return redirect(home)

        return render(request, template_name, {'formset':formset , 'dateDebut' : ToeicCourant.date_Debut})


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
            i=1       
            for form in formset: #On récupère chacune des réponses 
                reponse  = form.cleaned_data.get('question')
                if(i<=6):
                    data = dataToeic(i,1,idToeic,reponse)
                elif(i>=7 and i<=31) :
                    data = dataToeic(i,2,idToeic,reponse)
                elif(i>=32 and i<=70):
                    data = dataToeic(i,3,idToeic,reponse)
                elif(i>=71 and i<=100):
                    data = dataToeic(i,4,idToeic,reponse)
                elif(i>=101 and i<=130):
                    data = dataToeic(i,5,idToeic,reponse)
                elif(i>=131 and i<=146):
                    data = dataToeic(i,6,idToeic,reponse)
                elif(i>=147 and i<=200):
                    data = dataToeic(i,7,idToeic,reponse)
                questionForm = QuestionForm(data)
                questionForm.is_valid()
                print(questionForm.errors)
                questionForm.save()
                i+=1
                userReponses.append(question) #On met chacune des réponses dans une liste
        return redirect(home)
    return render(request, template_name, {'formset':formset })

def dataToeic(i,numPartie,idToeic,reponse):
    return {
            'id_Question' : i,
            'id_TOEIC' : idToeic,
            'id_SousPartie' : numPartie,
            'reponse_Juste' : reponse
        }


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
    toeicEnCours = TOEICEnCours.objects.all()
    toeicEnCoursT = []


    maintenant=datetime.now()

    list_idToeicEnCours = []
    for t in toeic : #Pour chaque toeic
        for tEc in toeicEnCours : #Pour chaque session
            if(t.id==tEc.id_TOEIC.id and t.id not in list_idToeicEnCours): 
                date_debut = (tEc.date_Debut)
                finSession = date_debut + timedelta(hours=2)
                if(estPlusGrandDate(date_debut,maintenant)  ) :
                    if estPlusGrandDate(maintenant,finSession):
                        list_idToeicEnCours.append(t.id) # ajoute l'id des toeics réellement en cours (<2)
                        toeicEnCoursT.append(tEc) # ajoute les toeics réellement en cours (<2)
    if request.method == 'GET': #Pour récupérer la page
        test = NomToeicForm(None)
        context ={
            "titre":"Liste de Toeic",
            "liste":toeic,
            "test" : test
        }
        context['list_idToeicEnCours']=list_idToeicEnCours
        context['toeicEnCours']=toeicEnCoursT
        return render(request,"listeToeic.html",context) 
    elif request.method == 'POST':
        if('toeic' in request.POST): # Pour lancer un TOEIC
            toeic = TOEIC.objects.filter(id=request.POST['toeic'])[0]
            data = {
                "id_TOEIC":toeic.id,
                "date_Debut":datetime.now(),
                "password":BaseUserManager().make_random_password()
                ## On enregistre le mot de passe généré  
            }
            toeicEnCoursForm = ToeicEnCoursForm(data)
            if(toeicEnCoursForm.is_valid()):
                toeicEnCoursForm.save()
            return redirect(home)
        else : 
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

def espace_eleve(request): # Quand la fonction est appelée elle a pris en paramètre un id_eleve et affiche les résultats aux toeic de l'élève concerné
    #scoretot = ScoreParPartie.objects.filter(id_Eleve=id_eleve).values('id_SousPartie__type_Partie').annotate('id_TOEIC').annotate(Sum('score'))

    ### Ici scoretot est le tableau, des des scores par parties et par toeic de l'élève qui a pour id id_eleve
    #scoretot = ScoreParPartie.objects.filter(id_Eleve=id_eleve).values('id_TOEIC','id_SousPartie__type_Partie','score')
    eleve = Eleve.objects.filter(user = request.user)[0]
    nomprenom=str(eleve)
    id_eleve = eleve.id

    listeR=[]
    listeL=[]
    listeTOT=[]
    Tout=[]
    listeDate=[]

    # On recupère le nom et le prenom
    test = list(ScoreParPartie.objects.filter(id_Eleve=id_eleve).values('id_Eleve__nom','id_Eleve__prenom'))
    
    if len(test)!=0:
    
        nom = test[0]["id_Eleve__nom"]
        prenom = test[0]['id_Eleve__prenom']

        ### scoretot recupère le nombre de bonne réponses par toeic passé et par partie de l'élève qui a pour id id_eleve
        scoretot = ScoreParPartie.objects.filter( # Query set
            id_Eleve=id_eleve).values('id_TOEICEnCours__id_TOEIC','id_SousPartie__type_Partie').annotate(
            score=Sum('score')).values('id_TOEICEnCours__id_TOEIC','id_SousPartie__type_Partie','score','date_Passage').order_by('date_Passage')

        #print(scoretot)
        ListeNoteParPartie = list(scoretot) # Transformation de la query set en list

        ##Ici on fait la liste qui contient les notes par partie
        for i in ListeNoteParPartie : 
            if i["id_SousPartie__type_Partie"]=="L":
                i["score"]=(NOTE_L(i["score"])) # Recuperation du score d'un dictionnaire et changement du score grace a la fonction de calcul
            else:
                i["score"]=(NOTE_R(i["score"]))
        #print("Listenoteparpartie",ListeNoteParPartie)

        

        #On créer la liste des notes Listening

        for i in ListeNoteParPartie :
            if i["id_SousPartie__type_Partie"]=="L":
                listeL.append(i["score"])
                listeDate.append(i["date_Passage"].strftime("%d-%b-%Y"))
            else:
                listeR.append(i["score"])

        #print('LISTER',listeR)
        #print('LISTEL',listeL)
        #Oncréer la liste des notes Total

        for i in range(len(listeR)):
            scoretot=listeR[i]+listeL[i]
            #nouveauquery= {'id_TOEIC': listeR[i]["id_TOEIC"], 'id_Eleve__nom': listeR[i]["id_Eleve__nom"], 'id_SousPartie__type_Partie': 'TOT', 'score': scoretot,'date_Passage':listeR[i]['date_Passage']}
            listeTOT.append(scoretot)

        for i in range(len(listeR)):
            Tout.append(listeR[i])
            Tout.append(listeL[i])
            Tout.append(listeTOT[i])
        #print("listeR: ",listeR,"listeTOT: ",listeTOT,"listeR: ",listeR,"listeDate: ",listeDate,"nom et prenom : ",nom,prenom)

        #context = {"reading":listeR,"listening":listeL,"total":listeTOT}
    formulaire = EntrerSession(None)
    utilisateur = request.user
    eleve = Eleve.objects.filter(user=utilisateur)[0]
    querry_toeicPasse=list(ScoreParPartie.objects.filter(id_Eleve=eleve ) )
    liste_ToeicPasse = []

    for score in querry_toeicPasse :
        if score.id_TOEICEnCours not in liste_ToeicPasse :
            print(liste_ToeicPasse)
            liste_ToeicPasse.append(score.id_TOEICEnCours)
    if request.method == "POST":
        
        data = request.POST.copy()
        pwd=data.get('password')
        print("PWD: ",pwd)   


        print(querry_toeicPasse)   
        print(liste_ToeicPasse,"dzadzaaz")   
        print(TOEICEnCours.objects.all())
        for i in list(TOEICEnCours.objects.all()):
            print(i not in liste_ToeicPasse, "fdsqfqs")
            if(i not in liste_ToeicPasse):
                if pwd == i.password:
                    return redirect('repondTOEIC',i.id)




    context = {"formulaire":formulaire,'NoteR':json.dumps(listeR),'NoteTOT':json.dumps(listeTOT),'NoteL':json.dumps(listeL),'listeDate':json.dumps(listeDate),'nomprenom':nomprenom}
        #print('CONNNNNNTEXTXTTTXXTT',context)
        #scoretot=scoretot.objects.values('id_TOEIC').annotate(score=Sum('score')).values('id_Toeic','id_Eleve__nom','id_SousPartie__type_Partie','score')
    maintenant=datetime.now()
    toeic = list(TOEICEnCours.objects.all())
    toeicDispos=[]
    querry_toeicPasse=ScoreParPartie.objects.all()
    list_toeicPasse=[]
    for  toeicPasse in querry_toeicPasse :
        if(toeicPasse.id_TOEICEnCours not in list_toeicPasse):
            list_toeicPasse.append(toeicPasse.id_TOEICEnCours)
    print(list_toeicPasse)
    for t in toeic:
        date_debut = (t.date_Debut)
        
        finSession = date_debut + timedelta(hours=2)
        #print(estPlusGrandDate(date_debut,maintenant) ,estPlusGrandDate(maintenant,finSession) )
        if(t not in list_toeicPasse):
            if(estPlusGrandDate(date_debut,maintenant)  ) :
                if estPlusGrandDate(maintenant,finSession):
                    toeicDispos.append(t) 

    context["liste"] = liste_ToeicPasse     

    return render(request,"espace_eleve/notes_toeic.html",context) 
    


def register(request):
    if(request.user.is_authenticated):
        return redirect(home)
    else:
        if request.method == 'GET':
            form = UserForm() # Formulaire pour l'éléve sans l'utilisateur
            formUser = UserCreationForm() #Formulaire pour creer l'utilisateur
            context = { 'form' : form , 'formUser' : formUser}
            return render(request,'registration/register.html', context)
        elif request.method == 'POST':

            form = UserForm(request.POST)
            formUser = UserCreationForm(request.POST)
            if form.is_valid() and formUser.is_valid():
                user = formUser.save() # sauvegarde direct dans la bdd
                login(request, user)
            
                post = form.save(commit=False) # Eleve.save() mais pas dans la bdd
                post.user = user #Attribution utilisateur a l'eleve
                post.save() #Save eleve bdd

                username = user.username
                password = user.password
                user = authenticate(username=username, password=password)

                return redirect(home)
            else:
                return redirect(register)
def logout_view(request):
    logout(request)
    return redirect(home)
        

    ### Vue dans laquelle on va utiliser le filtre SearchFilter
def search(request):
    user_list = ScoreParPartie.objects.all()
    user_filter = SearchFilter(request.GET, queryset=user_list)
    return render(request, 'espace_prof/search_user.html', {'filter': user_filter})

def filtre_note_par_partie(request):
    if request.user.is_superuser == False:
        return redirect(home)
    else :
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
        requeteR = user_filter.qs.filter(id_SousPartie__type_Partie='R').values('id_TOEICEnCours__id_TOEIC','id_Eleve').order_by('id_TOEICEnCours__id_TOEIC','id_Eleve').annotate(sommetot=Sum('score'))
        requeteL = user_filter.qs.filter(id_SousPartie__type_Partie='L').values('id_TOEICEnCours__id_TOEIC','id_Eleve').order_by('id_TOEICEnCours__id_TOEIC','id_Eleve').annotate(sommetot=Sum('score'))
    

        # On exprime transmet les données des queryset en liste pour être plus maniable, avec chartit problèmes pour les notes etc
        # du coup j'ai changé et utilisé highchart qui utilise les listes.
        # Certes moins efficace mais beaucoup plus maniable




        score1 = [0,0,0,0,0,0,0]
        cat1 = ["0","1","2","3","4","5","6"]
        moy1=0
        effectiftot=0
        print(requete1)
        for j in requete1:
            score1[j['score']]+=j['the_count'] #Pour un score on a un effectif de personne qui ont eu cette note
            moy1+=j['score']*j['the_count'] # La moyenne est la somme des points total 
            effectiftot+=j['the_count']    # sur l'effectif total
        
        # Ici on recup une liste des notes totales
        notes=[0]*effectiftot
        k=0
        for r in requeteR :
            notes[k]+=NOTE_R(r["sommetot"])
            k+=1
        k=0
        for l in requeteL :
            notes[k]+=NOTE_L(l["sommetot"])
            k+=1
        print('notes totales',notes)

        #On calcul le taux de réussite
        valide=0
        rate=0
        for i in range(len(notes)):
            if notes[i]<815:
                rate+=1
            else: 
                valide+=1
    
        
        
        
        score2=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        
        cat2 = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25"]
        moy2=0
        
        for j in requete2:
            score2[j['score']]+=j['the_count']
            moy2+=j['score']*j['the_count'] # La moyenne est la somme des points total 

        score3=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        cat3 = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39"]
        moy3=0
        for j in requete3:
            score3[j['score']]+=j['the_count']
            moy3+=j['score']*j['the_count'] # La moyenne est la somme des points total 
        
        score4=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        cat4 = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"]
        moy4=0
        for j in requete4:
            score4[j['score']]+=j['the_count']
            moy4+=j['score']*j['the_count'] # La moyenne est la somme des points total 
        
        score5=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        cat5 = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"]
        moy5=0
        for j in requete5:
            score5[j['score']]+=j['the_count']
            moy5+=j['score']*j['the_count'] # La moyenne est la somme des points total 
        
        score6 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        cat6 = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"]
        moy6=0
        for j in requete6:
            score6[j['score']]+=j['the_count']
            moy6+=j['score']*j['the_count'] # La moyenne est la somme des points total 
        
        score7=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        cat7 = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54"]
        moy7 = 0
        for j in requete7:
            score7[j['score']]+=j['the_count']
            moy7+=j['score']*j['the_count'] # La moyenne est la somme des points total 

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

        a=[0,1,2,3,4,5,6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
        for i in range(len(a)):
            a[i]=NOTE_L(a[i])
        print(a)
        R=[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 65, 70, 80, 85, 90, 95, 100, 110, 115, 120, 125, 130, 140, 145, 150, 160, 165, 170, 175, 180, 190, 195, 200, 210, 215, 220, 225, 230, 235, 240, 250, 255, 260, 265, 270, 280, 285, 290, 300, 305, 310, 320, 325, 330, 335, 340, 350, 355, 360, 365, 370, 380, 385, 390, 395, 400, 405, 410, 415, 420, 425, 430, 435, 445, 450, 455, 465, 470, 480, 485, 490, 495, 495, 495, 495]
        L=[5, 5, 5, 5, 5, 5, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 110, 115, 120, 125, 130, 135, 140, 145, 150, 160, 165, 170, 175, 180, 185, 190, 195, 200, 210, 215, 220, 230, 240, 245, 250, 255, 260, 270, 275, 280, 290, 295, 300, 310, 315, 320, 325, 330, 340, 345, 350, 360, 365, 370, 380, 385, 390, 395, 400, 405, 410, 420, 425, 430, 440, 445, 450, 460, 465, 470, 475, 480, 485, 490, 495, 495, 495, 495, 495, 495, 495, 495, 495, 495, 495]

        if effectiftot>0:
            ## On calcul les moyennes par parties

            moy1=moy1/effectiftot   
            moy2=moy2/effectiftot
            moy3=moy3/effectiftot
            moy4=moy4/effectiftot
            moy5=moy5/effectiftot
            moy6=moy6/effectiftot
            moy7=moy7/effectiftot

            ## On calcul les medianes par parties
            med1=mediane(score1,effectiftot)
            med2=mediane(score2,effectiftot)
            med3=mediane(score3,effectiftot)
            med4=mediane(score4,effectiftot)
            med5=mediane(score5,effectiftot)
            med6=mediane(score6,effectiftot)
            med7=mediane(score7,effectiftot)

            ## Calcul du taux de réussite total

            txReussite = float(valide)/effectiftot*100
            txEchec= 100.0-txReussite
        else:
            # On calcul les moyennes par parties

            moy1=0
            moy2=0
            moy3=0
            moy4=0
            moy5=0
            moy6=0
            moy7=0

            ## On calcul les medianes par parties
            med1=0
            med2=0
            med3=0
            med4=0
            med5=0
            med6=0
            med7=0

            ## Calcul du taux de réussite total

            txReussite =0
            txEchec= 0

        score1 = json.dumps(score1)
        cat1 = json.dumps(cat1)
        score2 = json.dumps(score2)
        cat2 = json.dumps(cat2)
        score3 = json.dumps(score3)
        cat3 = json.dumps(cat3)
        score4 = json.dumps(score4)
        cat4 = json.dumps(cat4)
        score5 = json.dumps(score5)
        cat5 = json.dumps(cat5)
        score6 = json.dumps(score6)
        cat6 = json.dumps(cat6)
        score7 = json.dumps(score7)
        cat7 = json.dumps(cat7)




        
        parties=["Partie 1","Partie 2","Partie 3","Partie 4","Partie 5","Partie 6","Partie7"]
        moyennes=[moy1,moy2,moy3,moy4,moy5,moy6,moy7]
        tauxMRParPartie=[100*med1/6,100*med2/25,100*med3/39,100*med4/30,100*med5/30,100*med6/16,100*med7/54]
        tauxRParPartie=[100*moy1/6,100*moy2/25,100*moy3/39,100*moy4/30,100*moy5/30,100*moy6/16,100*moy7/54]

        print("tauxMRParPartie",tauxMRParPartie)
        print("TRPP",tauxRParPartie)
        return render(request,'espace_prof/search_user.html',{"tauxMRParPartie":json.dumps(tauxMRParPartie),"tauxRParPartie":json.dumps(tauxRParPartie),"txEchec":json.dumps(txEchec),"txReussite":json.dumps(txReussite),'cat1':cat1,'score1':score1,'cat2':cat2,'score2':score2,'cat3':cat3,'score3':score3,'cat4':cat4,'score4':score4,'cat5':cat5,'score5':score5,'cat6':cat6,'score6':score6,'cat7':cat7,'score7':score7,'catR':catR,'scoreR':scoreR,'catL':catL,'scoreL':scoreL,'filter': user_filter})


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

def consulter_eleve(request):
    eleves_mea=[]
    eleves_ig=[]
    eleves = Eleve.objects.all().order_by('classe')
    for i in eleves:
        
        print(eleves)
    return render(request,"liste.html",{'liste':eleves}) 




