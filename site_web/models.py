from django.db import models
from django.db.models import Func
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager


#from site_web.fonctions_TOEIC import NOTE_L
# Create your models here.

class Classe(models.Model):
    lib_Classe=models.CharField(max_length=10)
    annee_Promo=models.CharField(max_length=9)
  
    def __str__(self):
        return self.lib_Classe

class Groupe(models.Model):
    lib_Groupe=models.CharField(max_length=5)

    def __str__(self):
        return self.lib_Groupe 

        
class Eleve(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom=models.CharField(max_length=50)
    prenom=models.CharField(max_length=50)
    classe=models.ForeignKey('Classe',default=None, on_delete=models.CASCADE) #Un élève appartient forcément à une classe
    groupe=models.ForeignKey('Groupe',default=None, on_delete=models.CASCADE) #Un élève appartient forcément un groupe peut-etre pas en cascade

    def __str__(self):
        return self.nom + " " + self.prenom

class TOEIC(models.Model):
    lib_TOEIC=models.CharField(max_length=20) 
    def __str__(self):
        return "Toeic : " +self.lib_TOEIC
class TOEICEnCours(models.Model):
    id_TOEIC=models.ForeignKey('TOEIC',default=None, on_delete=models.CASCADE) #La réponse à une question correspond à un Toeic 
    date_Debut = models.DateTimeField()
    password=BaseUserManager().make_random_password()
    def __str__(self):
        return "Session : " + self.id_TOEIC.lib_TOEIC + "Mot de passe: " + self.password


class Question(models.Model):
    id_Question=models.CharField(max_length=3 )
    id_TOEIC=models.ForeignKey('TOEIC',default=None, on_delete=models.CASCADE) #La réponse à une question correspond à un Toeic 
    id_SousPartie=models.ForeignKey('Sous_partie',default=None, on_delete=models.CASCADE) 
    reponse_Juste=models.CharField(max_length=1) #À revoir faire quelque chose de plus propre (énumeration ?)

    class Meta:
        unique_together = (("id_Question","id_TOEIC"),)
    def __str__(self):
        return str(self.id_TOEIC) + ", Sous partie :"+ str(self.id_SousPartie) +", question " + self.id_Question + " : " + self.reponse_Juste

class Sous_partie(models.Model): 
    lib_Partie=models.CharField(max_length=1) 
    type_Partie=models.CharField(max_length=15) 
    def __str__(self):
        return "Partie numéro : "+ self.lib_Partie +" " + self.type_Partie

class ScoreParPartie(models.Model): 
    id_Eleve=models.ForeignKey('Eleve',default=None, on_delete=models.CASCADE)  
    id_TOEICEnCours=models.ForeignKey('TOEICEnCours',default=None, on_delete=models.CASCADE)  
    id_SousPartie=models.ForeignKey('Sous_partie',default=None, on_delete=models.CASCADE) 
    date_Passage = models.DateTimeField()
    score=models.IntegerField() 
    class Meta:
        unique_together = (("id_SousPartie","id_TOEICEnCours","id_Eleve"),)
    def __str__(self):

        return "TOEIC : "+ str(self.id_TOEICEnCours.id_TOEIC) + "Partie : " + str(self.id_SousPartie) + " score de :" + str(self.score) + " Pour l'élève " + str(self.id_Eleve)
        #Fonction double cle primaire

    def note_L(self):
            if self.score > 60:
                  return 495
            return 0
