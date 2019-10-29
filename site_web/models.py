from django.db import models

# Create your models here.

class Classe(models.Model):
    lib_Classe=models.CharField(max_length=10)
    annee_Promo=models.CharField(max_length=4)
    def __unicode__(self):
        return self.lib_Classe    
    def __str__(self):
        return self.lib_Classe

        
class Eleve(models.Model):
    nom=models.CharField(max_length=50)
    prenom=models.CharField(max_length=50)
    classe=models.ForeignKey('Classe',default=None, on_delete=models.CASCADE)
    def __unicode__(self):
        return self.nom + " " + self.prenom
        
    def __str__(self):
        return self.nom + " " + self.prenom