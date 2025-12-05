from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from queueapp.models import QueueEntry
from queueapp.serializers import QueueEntrySerializer
from consultations.models import Consultation
from accounts.permissions import IsDoctor, IsAdmin, IsPatient


class QueueJoinView(APIView):
    permission_classes = [IsPatient]

    def post(self, request):
        patient = request.user.patientprofile
        if QueueEntry.objects.filter(patient=patient, status=QueueEntry.STATUS_WAITING).exists():
            return Response({"detail": "Paciente ja esta na fila."}, status=status.HTTP_400_BAD_REQUEST)
        payment = (
            patient.payments.filter(status="paid").order_by("-created_at").first()
            if hasattr(patient, "payments")
            else None
        )
        if not payment:
            return Response({"detail": "Pagamento aprovado necessario antes de entrar na fila."}, status=status.HTTP_402_PAYMENT_REQUIRED)
        consultation = Consultation.objects.create(patient=patient, payment=payment, status=Consultation.STATUS_WAITING)
        entry = QueueEntry.objects.create(patient=patient, consultation=consultation)
        return Response(QueueEntrySerializer(entry).data, status=status.HTTP_201_CREATED)


class QueueNextView(APIView):
    permission_classes = [IsDoctor | IsAdmin]

    def get(self, request):
        entry = QueueEntry.objects.filter(status=QueueEntry.STATUS_WAITING).order_by('joined_at').first()
        if not entry:
            return Response({'detail': 'Fila vazia'}, status=status.HTTP_200_OK)
        entry.status = QueueEntry.STATUS_SERVED
        entry.served_at = timezone.now()
        entry.consultation.status = Consultation.STATUS_ACTIVE
        entry.consultation.doctor = request.user.doctorprofile if hasattr(request.user, 'doctorprofile') else None
        entry.consultation.started_at = timezone.now()
        entry.consultation.save()
        entry.save()
        return Response(QueueEntrySerializer(entry).data)
