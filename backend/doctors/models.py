from django.db import models
from django.conf import settings
from utils.validators import validate_cpf


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctorprofile"
    )
    full_name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    crm_number = models.CharField(max_length=50)
    crm_state = models.CharField(max_length=2)
    specialty = models.CharField(max_length=100)
    workload_hours = models.PositiveIntegerField(default=0)
    digital_signature = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        validate_cpf(self.cpf)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.specialty}"
