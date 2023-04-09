from django import forms
from core.models import CustomUser

class RegisterForm(forms.ModelForm):

    repassword = forms.CharField(widget = forms.PasswordInput(attrs={'type': 'password' , 'placeholder':'Enter your repassword', 'name':'repassword'}))

    class Meta:

        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password','repassword' ]
        widgets = {
            "username" : forms.TextInput(attrs={'type':'text' , 'name':'username' , 'placeholder': 'Username'}),
            "first_name" : forms.TextInput(attrs={'type':'text' , 'name':'first_name' , 'placeholder': 'First Name'}),
            "last_name" : forms.TextInput(attrs={'type':'text' , 'name':'last_name' , 'placeholder': 'Last Name'}),
            "email":forms.TextInput(attrs={'type':'email' , 'name':'email' , 'placeholder': 'Email'}),
            "password" : forms.PasswordInput(attrs={'type':'password' , 'name':'password' , 'placeholder': 'Password'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs={'type': 'text' , 'placeholder':'Enter your username', 'name':'username'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'type': 'password' , 'placeholder':'Enter your password', 'name':'password'}))
