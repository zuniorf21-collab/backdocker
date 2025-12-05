from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from doctors.models import DoctorProfile
from utils.validators import validate_cpf

User = get_user_model()


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ['id', 'full_name', 'cpf', 'crm_number', 'crm_state', 'specialty', 'workload_hours', 'digital_signature', 'created_at']
        read_only_fields = ['id', 'created_at']


class DoctorCreateSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    cpf = serializers.CharField(max_length=14)
    crm_number = serializers.CharField(max_length=50)
    crm_state = serializers.CharField(max_length=2)
    specialty = serializers.CharField(max_length=100)
    workload_hours = serializers.IntegerField()
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, required=False)
    password = serializers.CharField(write_only=True)

    def validate_cpf(self, value):
        try:
            validate_cpf(value)
        except ValidationError as exc:
            raise serializers.ValidationError(exc.messages)
        if DoctorProfile.objects.filter(cpf=value).exists():
            raise serializers.ValidationError("CPF ja cadastrado para medico.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data['email']
        user = User.objects.create(email=email, username=email, role=User.Role.DOCTOR, phone=validated_data.get('phone'), cpf=validated_data['cpf'])
        user.set_password(password)
        user.save()
        doctor = DoctorProfile.objects.create(user=user, **validated_data)
        return doctor

    def to_representation(self, instance):
        return DoctorSerializer(instance).data
