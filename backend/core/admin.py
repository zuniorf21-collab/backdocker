from django.contrib import admin
from .models import User, Patient, Doctor, QueueEntry, Consultation, Document, AuditLog


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_staff")
    search_fields = ("username", "email")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "cpf", "email", "phone", "created_at")
    search_fields = ("full_name", "cpf", "email")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "crm", "specialty")
    search_fields = ("full_name", "crm")


@admin.register(QueueEntry)
class QueueEntryAdmin(admin.ModelAdmin):
    list_display = ("patient", "status", "created_at")
    list_filter = ("status",)


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "status", "started_at")
    list_filter = ("status",)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("consultation", "doc_type", "created_at")


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("action", "user", "target_type", "target_id", "success", "created_at")
    list_filter = ("action", "success")
    search_fields = ("target_type", "target_id", "user__username")
