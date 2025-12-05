from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "role", "is_active", "is_staff")
    search_fields = ("email", "cpf")
    list_filter = ("role", "is_active", "is_staff")
