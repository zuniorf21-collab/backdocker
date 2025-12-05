from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from patients.models import PatientProfile
from utils.validators import validate_cpf

User = get_user_model()


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ['id', 'full_name', 'cpf', 'birth_date', 'sex', 'street', 'number', 'district', 'zip_code', 'city', 'state', 'phone', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']


class PatientRegistrationSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    cpf = serializers.CharField(max_length=14)
    birth_date = serializers.DateField()
    sex = serializers.ChoiceField(choices=PatientProfile.SEX_CHOICES)
    street = serializers.CharField(max_length=255)
    number = serializers.CharField(max_length=20)
    district = serializers.CharField(max_length=255)
    zip_code = serializers.CharField(max_length=10)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=2)
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_cpf(self, value):
        try:
            validate_cpf(value)
        except ValidationError as exc:
            raise serializers.ValidationError(exc.messages)
        if User.objects.filter(cpf=value).exists() or PatientProfile.objects.filter(cpf=value).exists():
            raise serializers.ValidationError("CPF ja cadastrado.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data['email']
        user = User.objects.create(email=email, username=email, role=User.Role.PATIENT, cpf=validated_data['cpf'], phone=validated_data['phone'])
        user.set_password(password)
        user.save()
        patient = PatientProfile.objects.create(user=user, **validated_data)
        return patient

    def to_representation(self, instance):
        return PatientSerializer(instance).data
