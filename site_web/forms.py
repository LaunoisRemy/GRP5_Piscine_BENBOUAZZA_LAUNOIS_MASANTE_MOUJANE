from django import forms
from django.forms import formset_factory

class qcm(forms.Form):
    CHOICES = (('a','a'),
               ('b','b'),
               ('c','c'),
               ('d','d'),)
    question = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

qcmFormSet = formset_factory(qcm, extra=4) #Création d'un TOEIC de 4 questions