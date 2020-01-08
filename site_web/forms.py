from django import forms
from django.forms import formset_factory
from .models import *

class qcm(forms.Form):
    CHOICES = (('a','a'),
               ('b','b'),
               ('c','c'),
               ('d','d'),)
    question = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), initial=('a','a'))

qcmFormSet = formset_factory(qcm, extra=200) #Création d'un TOEIC de 4 questions

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
class ToeicForm(forms.ModelForm):
    class Meta:
        model = TOEIC
        fields = '__all__'

class ScoreParPartieForm(forms.ModelForm):
    class Meta:
        model = ScoreParPartie
        fields = '__all__'

class NomToeicForm(forms.Form):
    nom = forms.CharField(label='Nom du toeic : ', required=True,widget=forms.TextInput(attrs={'required': "required"}), max_length=100 )

class UserForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = ["nom","prenom","classe","groupe"]
    

