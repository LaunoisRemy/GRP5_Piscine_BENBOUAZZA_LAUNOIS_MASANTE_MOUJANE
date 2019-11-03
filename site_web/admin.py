from django.contrib import admin

# Register your models here.
from .models import *

class EleveAdmin(admin.ModelAdmin):
    class Meta:
        model=Eleve
    fieldsets=[
        ("Eleve",{"fields" : ["nom","prenom"]}),
        ("Classe",{"fields" : ["classe"]}),
        ("Groupe",{"fields":["groupe"]}),
        ("TOEIC",{"fields":["libelleTOEIC"]})
        #("Question",{"fields":["reponse_Juste"]})

    ]
#admin.site.register(Eleve,EleveAdmin)
admin.site.register(Eleve)
admin.site.register(Classe)
admin.site.register(TOEIC)
admin.site.register(Question)
admin.site.register(Groupe)