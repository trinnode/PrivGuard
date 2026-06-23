from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "full_name", "role", "is_active", "consent_granted", "date_joined")
    list_filter = ("role", "is_active", "consent_granted")
    search_fields = ("email", "full_name")
    ordering = ("-date_joined",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name", "institution")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "role")}),
        ("Consent", {"fields": ("consent_granted", "consent_date")}),
        ("Important dates", {"fields": ("last_login", "date_joined", "last_password_reset")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role", "consent_granted"),
        }),
    )
