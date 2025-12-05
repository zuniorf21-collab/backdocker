from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from patients.serializers import PatientRegistrationSerializer, PatientSerializer
from accounts.serializers import AdminUserCreateSerializer
from accounts.permissions import IsAdmin, IsPatient

User = get_user_model()


class PatientRegistrationView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PatientRegistrationSerializer


class MeView(generics.RetrieveAPIView):
    permission_classes = [IsPatient]
    serializer_class = PatientSerializer

    def get_object(self):
        return self.request.user.patientprofile


class AdminUserCreateView(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = AdminUserCreateSerializer
