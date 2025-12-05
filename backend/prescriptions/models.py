from django.db import models


class Prescription(models.Model):
    patient = models.ForeignKey('patients.PatientProfile', on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey('doctors.DoctorProfile', on_delete=models.CASCADE, related_name='prescriptions')
    consultation = models.ForeignKey('consultations.Consultation', on_delete=models.CASCADE, related_name='prescriptions')
    content = models.TextField()
    qr_code_data = models.TextField(blank=True)
    pdf_content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receita {self.id} - {self.patient.full_name}"
