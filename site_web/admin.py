from django.contrib import admin

# Register your models here.
from .models import *

class EleveAdmin(admin.ModelAdmin):
    class Meta:
        model=Eleve
    fieldsets=[
        ("Eleve",{"fields" : ["nom","prenom","num_INE"]}),
        ("Appartient",{"fields" : ["classe","groupe"]})
    ]
admin.site.register(Eleve,EleveAdmin)
admin.site.register(Classe)
admin.site.register(Groupe)
admin.site.register(Question)
admin.site.register(TOEIC)
admin.site.register(Sous_partie)

