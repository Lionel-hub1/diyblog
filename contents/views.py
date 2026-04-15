"""Views for the contents app."""
import os
import uuid

from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, Comment, Type
from .serializers import (
    ArticleSerializer,
    ArticleWithCommentsSerializer,
    CommentSerializer,
    RichTextImageUploadSerializer,
    TypeSerializer,
)


class IsAuthorOrStaff(permissions.BasePermission):
    """Allows access only to authenticated users with author/staff privileges."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_author or user.is_staff or user.is_superuser)
        )


class IsOwnerOrStaffOrReadOnly(permissions.BasePermission):
    """Object-level permission for mutating only owned articles unless staff."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_staff or user.is_superuser or obj.author_id == user.id)
        )


def index(request):
    return render(request, "index.html")


class ArticlesAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.select_related("type", "author").prefetch_related("comment_set")
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthorOrStaff()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ArticleWithCommentsSerializer
        return ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class OneArticleAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.select_related("type", "author")
    serializer_class = ArticleSerializer
    lookup_field = "id"
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [IsAuthorOrStaff(), IsOwnerOrStaffOrReadOnly()]


class TypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Type.objects.all().order_by("name")
    serializer_class = TypeSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthorOrStaff()]
        return [permissions.AllowAny()]


class ArticleCommentsAPIView(APIView):
    parser_classes = (JSONParser,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, id):
        article = get_object_or_404(Article, id=id)
        comments = article.comment_set.all().order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        get_object_or_404(Article, id=id)
        payload = request.data.copy()
        payload["article"] = id
        serializer = CommentSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateCommentAPIView(APIView):
    """Backward-compatible endpoint for creating comments."""

    parser_classes = (JSONParser,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({"message": "Comment endpoint expects POST."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request):
        return Response({"message": "Comment endpoint expects POST."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class RichTextImageUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthorOrStaff,)

    def post(self, request):
        serializer = RichTextImageUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        image = serializer.validated_data["image"]
        extension = os.path.splitext(image.name)[1].lower()
        generated_name = f"rich_text_images/{uuid.uuid4().hex}{extension}"
        saved_path = default_storage.save(generated_name, image)
        absolute_url = request.build_absolute_uri(default_storage.url(saved_path))
        return Response({"url": absolute_url}, status=status.HTTP_201_CREATED)


def about(request):
    return render(request, "about.html")


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")
