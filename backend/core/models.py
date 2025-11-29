from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = (
        ("patient", "Paciente"),
        ("doctor", "Médico"),
        ("admin", "Admin"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="patient")
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient")
    full_name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    birth_date = models.DateField()
    address = models.TextField()
    symptom_initial = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.full_name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor")
    full_name = models.CharField(max_length=255)
    crm = models.CharField(max_length=50)
    specialty = models.CharField(max_length=100, blank=True)
    digital_signature = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return f"{self.full_name} - CRM {self.crm}"


class QueueEntry(models.Model):
    STATUS_CHOICES = (
        ("waiting", "Esperando"),
        ("in_progress", "Atendendo"),
        ("finished", "Finalizado"),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="queue_entries")
    created_at = models.DateTimeField(auto_now_add=True)
    symptom = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="waiting")
    consultation = models.OneToOneField(
        "Consultation", on_delete=models.SET_NULL, null=True, blank=True, related_name="queue_entry"
    )

    def __str__(self) -> str:
        return f"{self.patient.full_name} - {self.status}"


class Consultation(models.Model):
    STATUS_CHOICES = (
        ("scheduled", "Agendada"),
        ("in_progress", "Em andamento"),
        ("finished", "Finalizada"),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="consultations")
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name="consultations")
    symptom = models.TextField()
    anamnesis = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    certificate = models.TextField(blank=True)
    declaration = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")
    room_name = models.CharField(max_length=100, blank=True)
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True, blank=True)

    def finish(self):
        self.status = "finished"
        self.finished_at = timezone.now()
        self.save()

    def __str__(self) -> str:
        return f"Consulta {self.id} - {self.patient.full_name}"


class Document(models.Model):
    TYPE_CHOICES = (
        ("anamnesis", "Anamnese"),
        ("prescription", "Receita"),
        ("certificate", "Atestado"),
        ("declaration", "Declaração"),
    )
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name="documents")
    doc_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    file = models.FileField(upload_to="documents/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.get_doc_type_display()} - {self.consultation_id}"


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ("login", "Login"),
        ("logout", "Logout"),
        ("create_patient", "Criação de paciente"),
        ("update_patient", "Alteração de dados"),
        ("queue_enter", "Entrada na fila"),
        ("consultation_start", "Início de consulta"),
        ("consultation_finish", "Fim de consulta"),
        ("pdf_generate", "Geração de PDF"),
        ("pdf_download", "Download de PDF"),
        ("whatsapp_send", "Envio pelo WhatsApp"),
        ("unauthorized_access", "Tentativa de acesso indevido"),
        ("record_update", "Alterações de prontuário"),
        ("document_update", "Alterações de documentos"),
        ("video_enter", "Entrada na sala de vídeo"),
        ("video_exit", "Saída da sala de vídeo"),
    ]

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    target_type = models.CharField(max_length=100, blank=True)
    target_id = models.CharField(max_length=100, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    success = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.action} by {self.user} at {self.created_at}"
