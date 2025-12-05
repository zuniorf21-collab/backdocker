from rest_framework import generics
from accounts.permissions import IsAdmin
from doctors.serializers import DoctorCreateSerializer, DoctorSerializer
from doctors.models import DoctorProfile


class DoctorCreateView(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = DoctorCreateSerializer


class DoctorListView(generics.ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = DoctorSerializer
    queryset = DoctorProfile.objects.all()
