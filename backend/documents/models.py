from django.db import models


class DocumentRecord(models.Model):
    TYPE_ATESTADO = "atestado"
    TYPE_ACOMPANHAMENTO = "declaracao_acompanhamento"
    TYPE_COMPARECIMENTO = "declaracao_comparecimento"
    TYPE_PRESCRICAO = "prescricao"

    TYPE_CHOICES = [
        (TYPE_ATESTADO, "Atestado"),
        (TYPE_ACOMPANHAMENTO, "Declaracao de Acompanhamento"),
        (TYPE_COMPARECIMENTO, "Declaracao de Comparecimento"),
        (TYPE_PRESCRICAO, "Prescricao"),
    ]

    consultation = models.ForeignKey("consultations.Consultation", on_delete=models.CASCADE)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="documents/")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.type} - {self.consultation_id}"
