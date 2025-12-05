from django.contrib import admin
from queueapp.models import QueueEntry


@admin.register(QueueEntry)
class QueueEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "status", "joined_at", "served_at")
    list_filter = ("status",)
