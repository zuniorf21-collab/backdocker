from django.db import models


class Certificate(models.Model):
    patient = models.ForeignKey('patients.PatientProfile', on_delete=models.CASCADE, related_name='certificates')
    doctor = models.ForeignKey('doctors.DoctorProfile', on_delete=models.CASCADE, related_name='certificates')
    consultation = models.ForeignKey('consultations.Consultation', on_delete=models.CASCADE, related_name='certificates')
    content = models.TextField()
    pdf_content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Atestado {self.id} - {self.patient.full_name}"
