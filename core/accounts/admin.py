from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, Profile


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom user in django admin page"""

    model = User
    list_display = [
        "email",
        "is_superuser",
        "is_active",
        "is_verified",
    ]

    list_filter = [
        "email",
        "is_superuser",
        "is_active",
        "is_verified",
    ]

    search_fields = ["email"]
    ordering = ["email"]

    # Detailed fields for viewing a user
    fieldsets = (
        (
            "Authentication",
            {
                "fields": (
                    "email",
                    "password",
                ),
            },
        ),
        (
            "Groups",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "is_verified",
                ),
            },
        ),
        (
            "logs",
            {
                "fields": ("last_login",),
            },
        ),
    )

    # Fields needed when creating a new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "is_verified",
                ),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = [
        "user",
        "username",
        "first_name",
        "last_name",
        "birth_date",
        "created_date",
        "updated_date",
    ]

    search_fields = ["username", "first_name", "last_name"]
    ordering = ["user"]
