from django import forms
from django.forms import ModelForm
from .models import User, Broker
# from django.core.validators import RegexValidator


class loginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}),)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class addBrokerForm(ModelForm):
    name = forms.CharField(label="Name", max_length=100, required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'Name'}), )
    ip = forms.GenericIPAddressField(label="Ip", max_length=100, required=True,
                                     widget=forms.TextInput(attrs={'placeholder': 'Ip Address'}), )
    description = forms.CharField(label="Description", max_length=100, required=True,
                                  widget=forms.TextInput(attrs={'placeholder': 'Broker description'}), )
    class Meta:
        model = Broker
        fields = ['name', 'ip', 'description']
