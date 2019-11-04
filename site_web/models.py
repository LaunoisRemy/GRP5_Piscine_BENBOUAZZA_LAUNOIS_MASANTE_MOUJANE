from django.db import models

# Create your models here.

class Classe(models.Model):
    lib_Classe=models.CharField(max_length=10)
    annee_Promo=models.CharField(max_length=4)
  
    def __str__(self):
        return self.lib_Classe

class Groupe(models.Model):
    lib_Groupe=models.CharField(max_length=5)

    def __str__(self):
        return self.lib_Groupe 

        
class Eleve(models.Model):
    num_INE=models.CharField(max_length=11,primary_key=True )
    nom=models.CharField(max_length=50)
    prenom=models.CharField(max_length=50)
    classe=models.ForeignKey('Classe',default=None, on_delete=models.CASCADE) #Un élève appartient forcément à une classe
    groupe=models.ForeignKey('Groupe',default=None, on_delete=models.CASCADE) #Un élève appartient forcément un groupe peut-etre pas en cascade

    def __str__(self):
        return self.nom + " " + self.prenom

class TOEIC(models.Model):
    lib_TOEIC=models.CharField(max_length=20)
    def __str__(self):
        return self.lib_TOEIC

class Question(models.Model):
<<<<<<< HEAD
    id_Question=models.CharField(max_length=1 )
    id_TOEIC=models.ForeignKey('TOEIC',default=None, on_delete=models.CASCADE) #La réponse à une question correspond à un Toeic 
    id_SousPartie=models.ForeignKey('Sous_partie',default=None, on_delete=models.CASCADE) 
=======
    id_TOEIC=models.ForeignKey('TOEIC',default=None, on_delete=models.CASCADE) #La réponse à une question correspond à un Toeic + (faut-il représenter la relativité ?)
    
    #id_Souspartie=models.ForeignKey('sous_Partie',default=None, on_delete=models.CASCADE) #Une réponse est comparée à une réponse d'une sous partie
>>>>>>> 2071f5ae17ed34bc3c01fc0c3798bd0b6251d34a
    reponse_Juste=models.CharField(max_length=1) #À revoir faire quelque chose de plus propre (énumeration ?)

    class Meta:
        unique_together = (("id_Question","id_TOEIC"),)
    def __str__(self):
        return str(self.id_TOEIC) + ", question " + self.id_Question + " : " + self.reponse_Juste

class Sous_partie(models.Model): 
    lib_Partie=models.CharField(max_length=1) 
    type_Partie=models.CharField(max_length=15) 
    def __str__(self):
        return "Partie numéro : "+ self.lib_Partie +" " + self.type_Partie

class Reponse(models.Model): 
    num_Ine=models.ForeignKey('Eleve',default=None, on_delete=models.CASCADE)  
    id_TOEIC=models.ForeignKey('TOEIC',default=None, on_delete=models.CASCADE)  
    id_SousPartie=models.ForeignKey('Sous_partie',default=None, on_delete=models.CASCADE) 
    score=models.CharField(max_length=2) 
    def __str__(self):
<<<<<<< HEAD
        return "TOEIC : "+self.id_TOEIC +"Partie : " + self.id_SousPartie + " score de :" + self.scoreqX
=======
        return str(self.id )+ ":" + self.reponse_Juste
>>>>>>> 2071f5ae17ed34bc3c01fc0c3798bd0b6251d34a

class Date(models.Model):#surment inutile
    date=models.DateField()

    def __str__(self):
        return self.date