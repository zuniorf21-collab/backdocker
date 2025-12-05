import uuid

from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from consultations.models import Consultation, MedicalRecordEntry
from consultations.twilio_service import (
    TwilioNotConfigured,
    TwilioVideoError,
    create_room_and_token,
    is_configured as twilio_is_configured,
)


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['id', 'patient', 'doctor', 'payment', 'status', 'scheduled_at', 'started_at', 'ended_at', 'twilio_room_name', 'twilio_token', 'recording_url', 'diagnosis', 'cid10', 'notes', 'created_at']
        read_only_fields = ['id', 'started_at', 'ended_at', 'twilio_room_name', 'twilio_token', 'recording_url', 'created_at']


class ConsultationStartSerializer(serializers.Serializer):
    doctor_id = serializers.IntegerField(required=False, allow_null=True)

    def update(self, instance, validated_data):
        instance.status = Consultation.STATUS_ACTIVE
        identity = self.context["request"].user.email or f"user-{self.context['request'].user.id}"
        if twilio_is_configured():
            try:
                room_name, token = create_room_and_token(identity)
                instance.twilio_room_name = room_name
                instance.twilio_token = token
            except (TwilioVideoError, TwilioNotConfigured) as exc:
                if not settings.DEBUG:
                    raise serializers.ValidationError({"detail": f"Erro ao criar sala de video: {exc}"})
                # fallback seguro em desenvolvimento
                instance.twilio_room_name = f"room-{uuid.uuid4().hex[:8]}"
                instance.twilio_token = uuid.uuid4().hex
        else:
            instance.twilio_room_name = f"room-{uuid.uuid4().hex[:8]}"
            instance.twilio_token = uuid.uuid4().hex
        instance.started_at = timezone.now()
        if validated_data.get('doctor_id'):
            instance.doctor_id = validated_data['doctor_id']
        instance.save()
        return instance


class ConsultationEndSerializer(serializers.Serializer):
    recording_url = serializers.URLField(required=False, allow_blank=True)
    diagnosis = serializers.CharField(required=False, allow_blank=True)
    cid10 = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def update(self, instance, validated_data):
        instance.status = Consultation.STATUS_COMPLETED
        instance.ended_at = timezone.now()
        for field in ['recording_url', 'diagnosis', 'cid10', 'notes']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()
        return instance


class MedicalRecordEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecordEntry
        fields = ['id', 'patient', 'consultation', 'author', 'entry_type', 'content', 'cid10', 'attachments', 'created_at']
        read_only_fields = ['id', 'created_at', 'author']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
