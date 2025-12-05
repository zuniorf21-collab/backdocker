from django.contrib import admin
from consultations.models import Consultation, MedicalRecordEntry


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "doctor", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("patient__full_name",)


@admin.register(MedicalRecordEntry)
class MedicalRecordEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "entry_type", "created_at")
    list_filter = ("entry_type",)
    search_fields = ("patient__full_name",)
