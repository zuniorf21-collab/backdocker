from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from consultations.models import Consultation, MedicalRecordEntry
from consultations.serializers import ConsultationSerializer, ConsultationStartSerializer, ConsultationEndSerializer, MedicalRecordEntrySerializer
from accounts.permissions import IsDoctor, IsAdmin, IsPatient
from doctors.models import DoctorProfile


class ConsultationStartView(APIView):
    permission_classes = [IsDoctor | IsAdmin]

    def post(self, request, pk):
        consultation = get_object_or_404(Consultation, pk=pk)
        if consultation.status not in [Consultation.STATUS_WAITING, Consultation.STATUS_PENDING]:
            return Response({"detail": "Consulta nao pode ser iniciada nesse status."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ConsultationStartSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        doctor_profile = getattr(request.user, "doctorprofile", None)
        if doctor_profile:
            consultation.doctor = doctor_profile
        else:
            doctor_id = serializer.validated_data.get("doctor_id")
            if not doctor_id:
                raise PermissionDenied("Administrador precisa informar doctor_id.")
            consultation.doctor = get_object_or_404(DoctorProfile, pk=doctor_id)
        serializer.update(consultation, serializer.validated_data)
        return Response(ConsultationSerializer(consultation).data)


class ConsultationEndView(APIView):
    permission_classes = [IsDoctor | IsAdmin]

    def post(self, request, pk):
        consultation = get_object_or_404(Consultation, pk=pk)
        if consultation.status != Consultation.STATUS_ACTIVE:
            return Response({"detail": "Apenas consultas ativas podem ser encerradas."}, status=status.HTTP_400_BAD_REQUEST)
        if consultation.doctor and hasattr(request.user, "doctorprofile") and consultation.doctor != request.user.doctorprofile:
            raise PermissionDenied("Somente o medico responsavel ou admin pode encerrar.")
        serializer = ConsultationEndSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(consultation, serializer.validated_data)
        return Response(ConsultationSerializer(consultation).data)


class ConsultationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctorprofile'):
            return Consultation.objects.filter(doctor=user.doctorprofile)
        if hasattr(user, 'patientprofile'):
            return Consultation.objects.filter(patient=user.patientprofile)
        if getattr(user, "role", None) == user.Role.ADMIN or getattr(user, "is_superuser", False):
            return Consultation.objects.all()
        return Consultation.objects.none()

    def perform_create(self, serializer):
        if not hasattr(self.request.user, "patientprofile"):
            raise PermissionDenied("Somente pacientes podem criar consultas.")
        serializer.save(patient=self.request.user.patientprofile)


class MedicalRecordEntryViewSet(generics.ListCreateAPIView):
    serializer_class = MedicalRecordEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'patientprofile'):
            return MedicalRecordEntry.objects.filter(patient=user.patientprofile)
        if hasattr(user, 'doctorprofile'):
            return MedicalRecordEntry.objects.filter(consultation__doctor=user.doctorprofile)
        if getattr(user, "role", None) == user.Role.ADMIN or getattr(user, "is_superuser", False):
            return MedicalRecordEntry.objects.all()
        return MedicalRecordEntry.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if not (hasattr(user, "doctorprofile") or getattr(user, "role", None) == user.Role.ADMIN or getattr(user, "is_superuser", False)):
            raise PermissionDenied("Somente medicos ou admins podem registrar evolucoes.")
        serializer.save(author=user)
