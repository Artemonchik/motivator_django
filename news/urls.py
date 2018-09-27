from django.contrib import admin
from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.start),
    path('news/', views.all_news, name='all_news'),
    path('reg/',views.sign_up, name='reg'),
    path('login/',views.sign_in, name='login'),
    path('new_post/', views.new_post, name='new_post'),
    path('follow_me/', views.follow_me, name='follow_me'),
    path('new_follow/<int:id>/', views.new_follow, name='new_follow'),
    path('myfollows/', views.myfollows, name='myfollows'),
    path('new_news/', views.new_news, name='new_news'),
    path('popular_news/', views.popular_news, name='popular_news'),
    path('follow_i/', views.follow_i, name='follow_i'),
    path('exit/', views.exit, name='exit'),
    path('dialog/', views.dialog, name='empty_dialog'),
    path('dialog/<int:id>/', views.messages, name='dialog'),
    path('like/post/<int:id>/', views.likepost, name='like'),
    path('unlike/post/<int:id>/', views.unlikepost, name='unlike'),
    path('check_messages/',views.checkMessage, name='check_message'),
    path('new_password', views.new_password, name='new_password')
]