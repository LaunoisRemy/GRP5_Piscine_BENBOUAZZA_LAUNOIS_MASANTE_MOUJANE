from django.contrib import admin

# Register your models here.
from .models import *

class EleveAdmin(admin.ModelAdmin):
    class Meta:
        model=Eleve
    fieldsets=[
        ("Eleve",{"fields" : ["nom","prenom"]}),
        ("Classe",{"fields" : ["classe"]})

    ]
admin.site.register(Eleve,EleveAdmin)
admin.site.register(Classe)