from django.db import models


class QueueEntry(models.Model):
    STATUS_WAITING = 'waiting'
    STATUS_SERVED = 'served'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_WAITING, 'Aguardando'),
        (STATUS_SERVED, 'Atendido'),
        (STATUS_CANCELLED, 'Cancelado'),
    ]
    patient = models.ForeignKey('patients.PatientProfile', on_delete=models.CASCADE, related_name='queue_entries')
    consultation = models.OneToOneField('consultations.Consultation', on_delete=models.CASCADE, related_name='queue_entry')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_WAITING)
    joined_at = models.DateTimeField(auto_now_add=True)
    served_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['joined_at']

    def __str__(self):
        return f"{self.patient.full_name} - {self.status}"
