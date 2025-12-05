from django.db import models
from django.conf import settings


class Consultation(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_WAITING = 'waiting'
    STATUS_ACTIVE = 'active'
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pendente"),
        (STATUS_WAITING, "Fila"),
        (STATUS_ACTIVE, "Em atendimento"),
        (STATUS_COMPLETED, "Concluida"),
        (STATUS_CANCELLED, "Cancelada"),
    ]
    patient = models.ForeignKey('patients.PatientProfile', on_delete=models.CASCADE, related_name='consultations')
    doctor = models.ForeignKey('doctors.DoctorProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='consultations')
    payment = models.OneToOneField('payments.Payment', on_delete=models.SET_NULL, null=True, blank=True, related_name='consultation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    twilio_room_name = models.CharField(max_length=120, blank=True)
    twilio_token = models.CharField(max_length=255, blank=True)
    recording_url = models.URLField(blank=True)
    diagnosis = models.TextField(blank=True)
    cid10 = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consulta {self.id} - {self.patient.full_name}"


class MedicalRecordEntry(models.Model):
    ENTRY_TYPES = (
        ("note", "Evolucao"),
        ("diagnosis", "Diagnostico"),
        ("prescription", "Receita"),
        ("certificate", "Atestado"),
    )
    patient = models.ForeignKey("patients.PatientProfile", on_delete=models.CASCADE, related_name="records")
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name="records")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPES)
    content = models.TextField()
    cid10 = models.CharField(max_length=20, blank=True)
    attachments = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.entry_type} - {self.patient.full_name}"
