from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class Registration(UserCreationForm):
    name = forms.CharField(max_length=20, widget=forms.TextInput())
    surname = forms.CharField(max_length=20, widget=forms.TextInput())
    email = forms.EmailField(max_length=30, widget=forms.EmailInput())
    image = forms.ImageField()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)


class SignIn(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Введите Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))


class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'time', 'image')


class NewMessage(forms.Form):
    message = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Введите сообщение',
                                                                            'autocomplete': 'off'}))
