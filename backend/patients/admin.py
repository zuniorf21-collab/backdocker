from django.contrib import admin
from patients.models import PatientProfile


@admin.register(PatientProfile)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "cpf", "email", "created_at")
    search_fields = ("full_name", "cpf", "email")
