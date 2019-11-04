from django.contrib import admin

# Register your models here.
from .models import *

class EleveAdmin(admin.ModelAdmin):
    class Meta:
        model=Eleve
    fieldsets=[
<<<<<<< HEAD
        ("Eleve",{"fields" : ["nom","prenom","num_INE"]}),
        ("Appartient",{"fields" : ["classe","groupe"]})

    ]
admin.site.register(Eleve,EleveAdmin)
admin.site.register(Classe)
admin.site.register(Groupe)
admin.site.register(Question)
admin.site.register(TOEIC)
admin.site.register(Sous_partie)
=======
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
>>>>>>> 2071f5ae17ed34bc3c01fc0c3798bd0b6251d34a
