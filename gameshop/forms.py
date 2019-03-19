from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Games

class gameform(forms.ModelForm):
    #model = Games
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    link = forms.URLField(widget=forms.URLInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'rows':'3'}))
    price = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    highscore = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Games
        fields=['name','link','description','price','highscore','tags']

class signupform(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    role = forms.ChoiceField( choices = [("gamer", "Gamer"), ("developer", "Developer")])
    class Meta:
        model = User
        fields=['username','first_name','last_name','email','password1','password2', 'role']
