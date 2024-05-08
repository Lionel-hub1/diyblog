"""Views for the contents app."""
from django.shortcuts import render
from django.http import JsonResponse
from .models import Article
from .serializers import *
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "index.html")


@api_view(['GET', 'POST', 'DELETE'])
def OneArticleAPIView(request, id):
    article = Article.objects.get(id=id)
    serializer = ArticleSerializer(article)
    return JsonResponse(serializer.data, safe=False)


class ArticlesAPIView(generics.ListAPIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleWithCommentsSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def ArticleCommentsAPIView(request, id):
    if request.method == "GET":
        article = Article.objects.get(id=id)
        comments = article.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    if request.method == "DELETE":
        count = Comment.objects.filter(id=id).delete()
        return JsonResponse(
            {'message': f'{count[0]} Comments were deleted successfully!'},
            status=204,
        )

    return JsonResponse({'message': 'Comment was not found'}, status=404)


class CreateCommentAPIView(APIView):
    @csrf_exempt
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)
        print(data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def get(self, request):
        return JsonResponse({'message': 'Comment was not found'}, status=404)

    def delete(self, request):
        return JsonResponse({'message': 'Comment was not found'}, status=404)


def about(request):
    return render(request, "about.html")


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")
