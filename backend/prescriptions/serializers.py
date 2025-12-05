import qrcode
import io
import base64
from rest_framework import serializers
from prescriptions.models import Prescription
from consultations.models import MedicalRecordEntry


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'doctor', 'consultation', 'content', 'qr_code_data', 'pdf_content', 'created_at']
        read_only_fields = ['id', 'qr_code_data', 'pdf_content', 'created_at']

    def create(self, validated_data):
        obj = super().create(validated_data)
        qr = qrcode.make(f"RX-{obj.id}-{obj.patient.cpf}")
        buffer = io.BytesIO()
        qr.save(buffer, format='PNG')
        obj.qr_code_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        obj.pdf_content = f"Receita para {obj.patient.full_name}: {obj.content}"
        obj.save()
        MedicalRecordEntry.objects.create(
            patient=obj.patient,
            consultation=obj.consultation,
            author=obj.doctor.user,
            entry_type='prescription',
            content=obj.content,
        )
        return obj
