from django.contrib import admin
from certificates.models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "doctor", "created_at")
