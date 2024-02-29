from django.contrib import admin
from .models import *


admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Type)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "profession", "phone_number", "is_author", "is_staff")
    list_filter = ("is_author", "is_staff")
    search_fields = ("username", "first_name", "last_name", "profession", "phone_number")
    ordering = ("username",)
