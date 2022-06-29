from django.contrib import admin
from core.models import Card
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            None, {
                "fields": (
                    "name",
                    "email",
                    "password"
                )
            }
        ),
        (
            "Permissions", {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important dates", {
                "fields": (
                    "last_login",
                    "date_joined"
                )
            }
        ),
    )
    list_display = ("email", "name", "is_staff")
    search_fields = ("name", "email")
    ordering = ["email"]


class CardAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "created_at",
        "completed_at",

        "title",
        "text",

        "file",
        
        "votes",
        "src",
        "data",

        "author",
        "parent",
        "root",
        "next",
    ]
    ordering = ["-created_at"]


admin.site.register(User, CustomUserAdmin)
admin.site.register(Card, CardAdmin)
