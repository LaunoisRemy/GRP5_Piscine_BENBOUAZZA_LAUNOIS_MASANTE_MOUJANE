from django.db import models

# Create your models here.

class Classe(models.Model):
    lib_Classe=models.CharField(max_length=10)
    annee_Promo=models.CharField(max_length=4)
  
    def __str__(self):
        return self.lib_Classe

class Groupe(models.Model):
    lib_Groupe=models.CharField(max_length=5)

    def __unicode__(self):
        return self.lib_Groupe 

        
class Eleve(models.Model):
    nom=models.CharField(max_length=50)
    prenom=models.CharField(max_length=50)
    classe=models.ForeignKey('Classe',default=None, on_delete=models.CASCADE) #Un élève appartient forcément à une classe
    groupe=models.ForeignKey('Groupe',default=None, on_delete=models.CASCADE) #Un élève appartient forcément un groupe

    def __str__(self):
        return self.nom + " " + self.prenom

class TOEIC(models.Model):
    LibelleTOEIC=models.CharField(max_length=20)

class Question(models.Model):
    id_TOEIC=models.ForeignKey('TOEIC',default=None, on_delete=models.CASCADE) #La réponse à une question correspond à un Toeic + (faut-il représenter la relativité ?)
    
    #id_Souspartie=models.ForeignKey('sous_Partie',default=None, on_delete=models.CASCADE) #Une réponse est comparée à une réponse d'une sous partie
    reponse_Juste=models.CharField(max_length=1) #À revoir faire quelque chose de plus propre (énumeration ?)

    def __str__(self):
        return str(self.id )+ ":" + self.reponse_Juste

class Date(models.Model):
    date=models.DateField()

    def __str__(self):
        return self.date