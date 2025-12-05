from rest_framework import serializers
from certificates.models import Certificate
from consultations.models import MedicalRecordEntry


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'patient', 'doctor', 'consultation', 'content', 'pdf_content', 'created_at']
        read_only_fields = ['id', 'pdf_content', 'created_at']

    def create(self, validated_data):
        obj = super().create(validated_data)
        obj.pdf_content = f"Atestado para {obj.patient.full_name}: {obj.content}"
        obj.save()
        MedicalRecordEntry.objects.create(
            patient=obj.patient,
            consultation=obj.consultation,
            author=obj.doctor.user,
            entry_type='certificate',
            content=obj.content,
        )
        return obj
