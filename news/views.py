from django.shortcuts import render, redirect
from . import forms
from .models import *
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# Create your views here.
def sign_up(request):

    if request.method == 'POST':
        form = forms.Registration(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            profile = Profile.objects.create(user=user)  # load the profile instance created by the signal
            user.profile.name = form.cleaned_data.get('name')
            user.profile.surname = form.cleaned_data.get('surname')
            user.email = form.cleaned_data.get('email')
            profile.profile_img = form.cleaned_data.get('image')
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
    return render(request, 'login/reg.html', {'form': form})


@login_required()
def all_news(request):
    if request.method == 'POST':
        #a = Post(author=request.user.profile)
        form = forms.NewPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.profile
            post.save()
            return HttpResponse('Спасибо большоооое')
        else:
            return HttpResponse('Что - то пошло не так. Убедитесь в правильности формы')
    else:
        form = forms.NewPost()
        count = Post.objects.count()
        posts = Post.objects.all()[::-1]
    return render(request, 'news/news.html', {'form': form,
                                              'posts': posts,
                                              'count': count,
                                              'profile': request.user.profile,
                                              'likes':request.user.profile.like_set.all(),
                                              })


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


def follow_me(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        follow_left = request.user.profile.follow_him.all()[0::2]
        follow_right = request.user.profile.follow_him.all()[1::2]
        return render(request, 'follows/subscriptions.html', {'profile': profile,
                                                              'follow_left': follow_left,
                                                              'follow_right': follow_right})
    else:
        return redirect('login')


def new_follow(request, id):
    if request.user.is_authenticated:
        profile = Profile.objects.get(id=id)
        request.user.profile.follow_he.add(profile)
        return HttpResponse('Всё отлично')
    else:
        redirect('login')


@login_required
def myfollows(request):
    if request.method == 'POST':
        form = forms.NewPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.profile
            post.save()
            return redirect('all_news')
    else:
        form = forms.NewPost()
        count = Post.objects.count()
        posts = Post.objects.filter(author__in=request.user.profile.follow_he.all()).order_by('-pub_date')
    return render(request, 'news/news.html', {'form': form,
                                              'posts': posts,
                                              'count': count,
                                              'likes': request.user.profile.like_set.all(),
                                              })


def follow_i(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        follow_left = request.user.profile.follow_he.all()[0::2]
        follow_right = request.user.profile.follow_he.all()[1::2]
        return render(request, 'follows/subscriptions.html', {'profile': profile,
                                                              'follow_left': follow_left,
                                                              'follow_right': follow_right})
    else:
        return redirect('login')


def exit(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

def getDialog(request, id):
    user_to = get_object_or_404(Profile, pk=id)
    dialog = Dialog.objects.filter(users=user_to).filter(users=request.user.profile)
    return dialog[0]

@login_required
def messages(request, id):
    user_to = get_object_or_404(Profile, pk=id)
    dialog = Dialog.objects.filter(users=user_to).filter(users=request.user.profile)
    if request.user.profile == user_to:
        return HttpResponse("you can't write yourself")
    if dialog:
        dialog = dialog[0]
    else:
        dialog = Dialog()
        dialog.save()
        dialog.users.add(user_to, request.user.profile)
        dialog.save()

    if request.method == 'POST':
        form = forms.NewMessage(request.POST)
        if form.is_valid():
            message = Message.objects.create(text=form.cleaned_data.get('message'), sender=request.user.profile,
                                             dialog=dialog)
            message.save()
            form = forms.NewMessage()
    else:
        form = forms.NewMessage()
    dialogs = Dialog.objects.filter(users=request.user.profile)
    users = []
    for d in dialogs:
        for u in d.users.all():
            if u == request.user.profile:
                continue
            users.append(u)
    print(request.content_type)
    if(request.is_ajax()):
        return HttpResponse("successful")
    return render(request, 'message/mes.html', {'dialog': dialog.message_set.order_by('-date'),
                                                'his_profile': user_to,
                                                'form': form,
                                                'profile': request.user.profile,
                                                'users': users,
                                                'count':dialog.message_set.count(),
                                                })
@login_required
def dialog(request):
    dialogs = Dialog.objects.filter(users=request.user.profile)
    users = []
    for d in dialogs:
        for u in d.users.all():
            if u == request.user.profile:
                continue
            users.append(u)
    return render(request, 'message/empty_dialog.html',{'users': users,
                                                        'profile': request.user.profile,
                                                        } )


def start(request):
    return redirect('all_news')

@login_required
def likepost(request, id):
    user = request.user.profile
    post = Post.objects.get(pk=id)
    try:
        post.like_set.get(user=user)
    except ObjectDoesNotExist:
        Like.objects.create(post=post, user=user)
        post.likes += 1
        post.save()
    except MultipleObjectsReturned:
        Like.objects.all().delete()
    return HttpResponse("That's okey. we have %s likes %s" % (post.like_set.count(), post.likes))

@login_required
def unlikepost(request, id):
    user = request.user.profile
    post = Post.objects.get(pk=id)
    try:
        post.like_set.get(user=user)
        Like.objects.get(post=post, user=user).delete()
        post.likes -= 1
        post.save()
    except ObjectDoesNotExist:
        pass
    except MultipleObjectsReturned:
        pass
    return HttpResponse("That's okey. we have %s likes %s" % (post.like_set.count(), post.likes))

@login_required
def new_news(request):
    if request.method == 'POST':
        a = Post(author=request.user.profile)
        form = forms.NewPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.profile
            post.save()
            return HttpResponse('Спасибо большоооое')
        else:
            return HttpResponse('Что - то пошло не так. Убедитесь в правильности формы')
    else:
        form = forms.NewPost()
        count = Post.objects.count()
        posts = Post.objects.all().order_by('-pub_date')
    return render(request, 'news/news.html', {'form': form,
                                              'posts': posts,
                                              'count': count,
                                              'profile': request.user.profile,
                                              'likes':request.user.profile.like_set.all(),
                                              })

def popular_news(request):
    if request.method == 'POST':
        a = Post(author=request.user.profile)
        form = forms.NewPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.profile
            post.save()
            return HttpResponse('Спасибо большоооое')
        else:
            return HttpResponse('Что - то пошло не так. Убедитесь в правильности формы')
    else:
        form = forms.NewPost()
        count = Post.objects.count()
        posts = Post.objects.all().order_by('-likes')
    return render(request, 'news/news.html', {'form': form,
                                              'posts': posts,
                                              'count': count,
                                              'profile': request.user.profile,
                                              'likes':request.user.profile.like_set.all(),
                                              })
@login_required
def checkMessage(request):
    if(request.method == "GET"):
        if(not request.GET.get("id")  or not request.GET.get("count")):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        id = int(request.GET.get("id"))
        count = int(request.GET.get("count"))
        dialog = getDialog(request,id)
        if(dialog.message_set.count() <= count):
            return HttpResponse("No messages")
        else:
            str = ""
            messages1 = dialog.message_set.all()[count::]
            for i in messages1:
                str = str + i.text + ","
            str = str[:-1]

            response = HttpResponse(str,content_type="text/plain")
            return response

