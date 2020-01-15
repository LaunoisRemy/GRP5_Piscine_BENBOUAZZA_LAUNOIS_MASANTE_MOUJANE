from django import forms
from django.forms import formset_factory
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class qcm(forms.Form):
    CHOICES = (('a','a'),
               ('b','b'),
               ('c','c'),
               ('d','d'),)
    question = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(),initial=('c','c'))
class qcmEleve(forms.Form):
    CHOICES = (('a','a'),
               ('b','b'),
               ('c','c'),
               ('d','d'),)
    question = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(),initial=('b','b'))

qcmFormSet = formset_factory(qcm, extra=200) #Création d'un TOEIC de 200 questions
qcmEleveFormSet = formset_factory(qcmEleve, extra=200) #Création d'un TOEIC de 200 questions

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
class ToeicForm(forms.ModelForm):
    class Meta:
        model = TOEIC
        fields = '__all__'
class ToeicEnCoursForm(forms.ModelForm):
    class Meta:
        model = TOEICEnCours
        fields = '__all__'
class ScoreParPartieForm(forms.ModelForm):
    class Meta:
        model = ScoreParPartie
        fields = '__all__'

class NomToeicForm(forms.Form):
    nom = forms.CharField(label='Nom du toeic : ', required=True,widget=forms.TextInput(attrs={'required': "required"}), max_length=100 )

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class UserForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = ["nom","prenom","classe","groupe"]
    

class EntrerSession(forms.Form):
    password = forms.CharField(label='Code session : ', required=True,widget=forms.TextInput(attrs={'required': "required"}), max_length=100 )
