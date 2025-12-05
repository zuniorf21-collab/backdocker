from django.contrib import admin
from doctors.models import DoctorProfile


@admin.register(DoctorProfile)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "crm_number", "crm_state", "specialty")
    search_fields = ("full_name", "cpf", "crm_number")
