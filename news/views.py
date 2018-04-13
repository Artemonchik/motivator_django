from django.shortcuts import render, redirect
from . import forms
from .models import *
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        form = forms.Registration(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            profile=Profile.objects.create(user=user)# load the profile instance created by the signal
            user.profile.name = form.cleaned_data.get('name')
            user.profile.surname = form.cleaned_data.get('surname')
            user.email = form.cleaned_data.get('email')
            user.save()
            profile.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('all_news')
            else:
                return HttpResponse('Something wrong')
    else:
        form = forms.Registration()
    return render(request, 'login/reg.html', {'form' : form})


def all_news(request):
    if request.method == 'POST':
        a = Post(author=request.user.profile)
        form = forms.NewPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.profile
            post.save()
            return HttpResponse('Спасибо большоооое')
    else:
        form = forms.NewPost()
        posts = Post.objects.all()[::-1]
    return render(request, 'news/news.html', {'form': form,
                                              'posts': posts})


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('all_news')
    else:
        if request.method == 'POST':
            form = forms.SignIn(request.POST)
            if form.is_valid():
                user = authenticate(username=form.cleaned_data.get('username'),
                                    password=form.cleaned_data.get('password'))
                if user is not None:
                    login(request, user)
                    return redirect('all_news')
                else:
                    return HttpResponse('This user does not exist')
        else:
            form = forms.SignIn()
        return render(request, 'login/login.html', {'form': form})


def new_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            a = Post(author=request.user.profile)
            form = forms.NewPost(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user.profile
                post.save()
                return HttpResponse('Спасибо большоооое')
        else:
            form = forms.NewPost()
        return render(request, 'news/newpost.html', {'form': form})
    else:
        return HttpResponse('BAD')
