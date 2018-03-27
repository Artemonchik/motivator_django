from django.shortcuts import render

# Create your views here.


def all_news(request):
    return render(request, 'news/news.html')