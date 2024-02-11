"""Views for the contents app."""
from django.shortcuts import render
from .models import Article


def index(request):
    return render(request, "index.html")

def article(request, article_id):
    article = Article.objects.get(id=article_id)
    titles = Article.objects.all().values_list('title', flat=True)
    return render(request, "article.html", {"article": article})
    


def about(request):
    return render(request, "about.html")


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")
