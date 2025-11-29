from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Patient, Doctor, QueueEntry, Consultation, Document

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "phone"]
        read_only_fields = ["id", "role"]


class PatientRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = [
            "full_name",
            "cpf",
            "email",
            "phone",
            "birth_date",
            "address",
            "symptom_initial",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            role="patient",
            phone=validated_data.get("phone", ""),
            password=password,
        )
        patient = Patient.objects.create(user=user, **validated_data)
        return patient


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = [
            "id",
            "user",
            "full_name",
            "cpf",
            "email",
            "phone",
            "birth_date",
            "address",
            "symptom_initial",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "symptom_initial"]


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = ["id", "user", "full_name", "crm", "specialty", "digital_signature"]
        read_only_fields = ["id"]


class QueueEntrySerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = QueueEntry
        fields = ["id", "patient", "created_at", "symptom", "status", "consultation"]
        read_only_fields = ["id", "created_at", "status", "consultation"]


class QueueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueEntry
        fields = ["symptom"]


class ConsultationSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = Consultation
        fields = [
            "id",
            "patient",
            "doctor",
            "symptom",
            "anamnesis",
            "notes",
            "prescription",
            "certificate",
            "declaration",
            "status",
            "room_name",
            "started_at",
            "finished_at",
        ]
        read_only_fields = ["id", "patient", "doctor", "status", "started_at", "finished_at"]


class ConsultationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ["anamnesis", "notes", "prescription", "certificate", "declaration", "status"]


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "doc_type", "file", "created_at"]
        read_only_fields = ["id", "file", "created_at"]


class DocumentSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "doc_type", "file", "created_at"]
        read_only_fields = ["id", "file", "created_at"]


class ConsultationHistorySerializer(serializers.ModelSerializer):
    doctor_name = serializers.SerializerMethodField()
    documents = DocumentSummarySerializer(many=True, read_only=True, source="documents")

    class Meta:
        model = Consultation
        fields = [
            "id",
            "symptom",
            "anamnesis",
            "notes",
            "prescription",
            "certificate",
            "declaration",
            "status",
            "room_name",
            "started_at",
            "finished_at",
            "doctor_name",
            "documents",
        ]
        read_only_fields = [
            "id",
            "symptom",
            "anamnesis",
            "notes",
            "prescription",
            "certificate",
            "declaration",
            "status",
            "room_name",
            "started_at",
            "finished_at",
            "doctor_name",
            "documents",
        ]

    def get_doctor_name(self, obj):
        if obj.doctor:
            return obj.doctor.full_name
        return None
