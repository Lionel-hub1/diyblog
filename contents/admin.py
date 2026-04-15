from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Author, Comment, Type, User


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("created_at", "edited_at")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "type",
        "created_at",
        "edited_at",
        "image_preview",
    )
    list_filter = ("type", "author")
    search_fields = ("title", "author__username", "content")
    readonly_fields = ("image_preview", "created_at", "edited_at")
    inlines = [CommentInline]
    fieldsets = (
        (None, {"fields": ("title", "content", "type", "author")}),
        ("Media", {"fields": ("image", "image_preview")}),
        ("Dates", {"fields": ("created_at", "edited_at")}),
    )

    def image_preview(self, obj):
        if not obj:
            return ""
        image = getattr(obj, "image", None)
        if not image:
            return ""
        try:
            url = image.url
        except Exception:
            return ""
        return format_html('<img src="{}" style="max-height:120px;"/>', url)

    def save_model(self, request, obj, form, change):
        if not change and not getattr(obj, "author", None):
            obj.author = request.user
        super().save_model(request, obj, form, change)

    image_preview.short_description = "Image Preview"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "article", "author", "created_at")
    search_fields = ("author", "content")
    list_filter = ("article",)
    readonly_fields = ("created_at", "edited_at")


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username", "user__first_name", "user__last_name")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "profession",
        "phone_number",
        "is_author",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("is_author", "is_staff")
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "profession",
        "phone_number",
    )
    ordering = ("username",)
