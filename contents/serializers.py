from rest_framework import serializers
from .models import *


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'type',
                  'author', 'created_at', 'edited_at', 'image']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'article', 'author',
                  'content', 'created_at', 'edited_at']


class CommentsSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'article', 'author',
                  'content', 'created_at', 'edited_at']
        many = True


class ArticleWithCommentsSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer(many=True, source='comment_set')
    type = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'type', 'author',
                  'created_at', 'edited_at', 'image', 'comments']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['user']
