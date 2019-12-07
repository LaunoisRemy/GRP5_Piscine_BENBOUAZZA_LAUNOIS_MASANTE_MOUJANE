from django import forms

class qcm(forms.Form):
    CHOICES = (('a','a'),
               ('b','b'),
               ('c','c'),
               ('d','d'),)
    picked = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())


