from django import forms
from django.forms import ModelForm
from .models import User
# from django.core.validators import RegexValidator


class registerUserForm(ModelForm):
    username = forms.CharField(label="Username", max_length=100, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}),)
    email = forms.EmailField(label="Email", max_length=150, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email Address'}), )
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, min_length=1,
                                max_length=20, required=True,)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput, min_length=1,
                                max_length=20, required=True,)
    firstName = forms.CharField(label="First Name", max_length=100, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'First Name'}),)
    lastName = forms.CharField(label="Last Name", max_length=100, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'firstName', 'lastName']
        # widgets = { 'password' : forms.PasswordInput() }


class loginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}),)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


# class addBrokerForm(ModelForm):
#     name = forms.CharField(label="Name", max_length=100, required=True,
#                            widget=forms.TextInput(attrs={'placeholder': 'Name'}), )
#     ip = forms.GenericIPAddressField(label="Ip", max_length=100, required=True,
#                                      widget=forms.TextInput(attrs={'placeholder': 'Ip Address'}), )
#     description = forms.CharField(label="Description", max_length=100, required=True,
#                                   widget=forms.TextInput(attrs={'placeholder': 'Broker description'}), )
#     class Meta:
#         model = Broker
#         fields = ['name', 'ip', 'description']
