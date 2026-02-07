from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoAdmin

from apps.users.models import User, EmailVerification


class EmailVerificationInline(admin.TabularInline):
    model = EmailVerification
    extra = 0
    can_delete = False
    readonly_fields = ("token_hash", "expires_at", "attempts", "last_sent_at", "created_at", "used_at")
    fields = ("token_hash", "expires_at", "attempts", "last_sent_at", "created_at", "used_at")
    show_change_link = True


@admin.register(User)
class UserAdmin(DjangoAdmin):
    model = User
    list_display = ("email", "first_name", "last_name", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    ordering = ("email",)
    search_fields = ("email", "first_name", "last_name")
    inlines = (EmailVerificationInline,)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Role", {"fields": ("role",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "role", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "expires_at", "used_at", "attempts", "created_at")
    list_filter = ("used_at", "expires_at", "created_at")
    search_fields = ("user__email", "token_hash")
    ordering = ("-created_at",)
    readonly_fields = ("token_hash", "created_at", "used_at", "last_sent_at")
