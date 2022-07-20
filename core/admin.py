from django.contrib import admin
from core.models import User, Card, HTMLContent, GoogleDoc, MP4ImageViewer, SiteSettings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
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
        'created_at',
        'updated_at',
        'parent',
        'uuid',
        'site',
        'url',
        'title',
        'description',
        'published',
        'content_type',
        'object_id',
        'content_object',
    ]

    ordering = ["-created_at"]


class HTMLContentAdmin(admin.ModelAdmin):
    pass


class GoogleDocAdmin(admin.ModelAdmin):
    list_display = [
        'google_doc_title',
        'google_doc_url',
    ]


class MP4ImageViewerAdmin(admin.ModelAdmin):
    pass


class SiteSettingsAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, CustomUserAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(HTMLContent, HTMLContentAdmin)
admin.site.register(GoogleDoc, GoogleDocAdmin)
admin.site.register(MP4ImageViewer, MP4ImageViewerAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
