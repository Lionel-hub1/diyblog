import bleach
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from .models import Article, Author, Comment, Type, User

try:
    from bleach.css_sanitizer import CSSSanitizer
except ImportError:
    CSSSanitizer = None

RICH_TEXT_ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS.union(
    {
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "p",
        "span",
        "div",
        "pre",
        "code",
        "blockquote",
        "img",
        "br",
        "hr",
        "u",
        "s",
    }
)

RICH_TEXT_ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "target", "rel"],
    "img": ["src", "alt", "title", "width", "height", "style"],
    "*": ["class", "style"],
}

if CSSSanitizer is not None:
    RICH_TEXT_CSS_SANITIZER = CSSSanitizer(
        allowed_css_properties=[
            "color",
            "background-color",
            "text-align",
            "font-weight",
            "font-style",
            "text-decoration",
            "width",
            "height",
        ]
    )
else:
    RICH_TEXT_CSS_SANITIZER = None


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profession",
            "phone_number",
            "is_author",
            "is_staff",
            "is_superuser",
        ]


class UserCreateSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profession",
            "phone_number",
            "is_author",
            "password",
        ]


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source="type.name", read_only=True)
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "type",
            "type_name",
            "author",
            "created_at",
            "edited_at",
            "image",
        ]
        read_only_fields = ["id", "author",
                            "created_at", "edited_at", "type_name"]

    def validate_content(self, value):
        if not value:
            return value

        clean_kwargs = {
            "tags": RICH_TEXT_ALLOWED_TAGS,
            "attributes": RICH_TEXT_ALLOWED_ATTRIBUTES,
            "protocols": ["http", "https", "mailto", "data"],
            "strip": True,
        }

        if RICH_TEXT_CSS_SANITIZER is not None:
            clean_kwargs["css_sanitizer"] = RICH_TEXT_CSS_SANITIZER

        return bleach.clean(
            value,
            **clean_kwargs,
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "article", "author",
                  "content", "created_at", "edited_at"]
        read_only_fields = ["id", "created_at", "edited_at"]


class ArticleWithCommentsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(
        many=True, source="comment_set", read_only=True)
    type = serializers.StringRelatedField()
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "type",
            "author",
            "created_at",
            "edited_at",
            "image",
            "comments",
        ]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["user"]


class RichTextImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
