from django.contrib import admin
from audit.models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "path", "method", "created_at")
    list_filter = ("method",)
    search_fields = ("path", "user__email")
