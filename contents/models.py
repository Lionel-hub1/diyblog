from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    profession = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    is_author = models.BooleanField(default=False)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Type(models.Model):
    """Model for types of articles."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    """Model for articles."""
    title = models.CharField(max_length=255)
    content = models.TextField()
    type = models.ForeignKey(
        Type, on_delete=models.DO_NOTHING, null=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='article_images/')


class Author(models.Model):
    """Model for authors."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    """Model for comments on articles."""
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
