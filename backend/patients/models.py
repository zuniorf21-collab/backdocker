from django.db import models
from django.conf import settings
from utils.validators import validate_cpf


class PatientProfile(models.Model):
    SEX_CHOICES = (('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patientprofile')
    full_name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    birth_date = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    district = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        validate_cpf(self.cpf)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.cpf})"
