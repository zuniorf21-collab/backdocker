from rest_framework import viewsets, permissions
from certificates.models import Certificate
from certificates.serializers import CertificateSerializer
from accounts.permissions import IsDoctor


class CertificateViewSet(viewsets.ModelViewSet):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return Certificate.objects.filter(doctor=self.request.user.doctorprofile)

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctorprofile)
