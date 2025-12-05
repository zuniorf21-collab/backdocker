from django.contrib import admin
from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "status", "transaction_code", "created_at")
    list_filter = ("status",)
    search_fields = ("transaction_code",)
