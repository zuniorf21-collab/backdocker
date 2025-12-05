from rest_framework import viewsets, permissions
from prescriptions.models import Prescription
from prescriptions.serializers import PrescriptionSerializer
from accounts.permissions import IsDoctor


class PrescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return Prescription.objects.filter(doctor=self.request.user.doctorprofile)

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctorprofile)
