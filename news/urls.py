from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.all_news, name='all_news'),
    path('reg/',views.sign_up, name='reg'),
    path('login/',views.sign_in, name='login'),
    path('new_post/', views.new_post, name='new_post')
]