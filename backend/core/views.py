from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import FileResponse

from .models import Patient, Doctor, QueueEntry, Consultation, Document
from .serializers import (
    PatientRegistrationSerializer,
    PatientSerializer,
    QueueEntrySerializer,
    QueueCreateSerializer,
    ConsultationSerializer,
    ConsultationUpdateSerializer,
    DoctorSerializer,
    DocumentSerializer,
    ConsultationHistorySerializer,
)
from .permissions import IsDoctor, IsPatient
from .services import generate_pdf, build_document_payload, generate_twilio_video_token, send_whatsapp_message
from .audit import log_audit

User = get_user_model()


class RegisterPatientView(generics.CreateAPIView):
    serializer_class = PatientRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        patient = serializer.save()
        log_audit("create_patient", patient.user, target=patient, request=self.request)


class PatientMeView(generics.RetrieveAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsPatient]

    def get_object(self):
        return self.request.user.patient


class EnterQueueView(generics.CreateAPIView):
    serializer_class = QueueCreateSerializer
    permission_classes = [IsPatient]

    def perform_create(self, serializer):
        patient = self.request.user.patient
        entry = serializer.save(patient=patient, status="waiting")
        log_audit("queue_enter", self.request.user, target=entry, request=self.request)


class PatientQueueStatusView(generics.ListAPIView):
    serializer_class = QueueEntrySerializer
    permission_classes = [IsPatient]

    def get_queryset(self):
        return QueueEntry.objects.filter(patient=self.request.user.patient).order_by("-created_at")


class PatientDocumentsView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsPatient]

    def get_queryset(self):
        return Document.objects.filter(consultation__patient=self.request.user.patient).order_by("-created_at")


@api_view(["GET"])
@permission_classes([IsPatient])
def patient_dashboard(request):
    patient = request.user.patient
    consultations = (
        Consultation.objects.filter(patient=patient)
        .select_related("doctor")
        .prefetch_related("documents")
        .order_by("-started_at")
    )
    queue_entries = patient.queue_entries.order_by("-created_at")[:5]
    data = {
        "patient": PatientSerializer(patient).data,
        "consultations": ConsultationHistorySerializer(consultations, many=True).data,
        "queue": QueueEntrySerializer(queue_entries, many=True).data,
    }
    return Response(data)


class DoctorQueueView(generics.ListAPIView):
    serializer_class = QueueEntrySerializer
    permission_classes = [IsDoctor]

    def get_queryset(self):
        return QueueEntry.objects.select_related("patient").order_by("created_at")


class DoctorConsultationDetailView(generics.RetrieveAPIView):
    serializer_class = ConsultationSerializer
    permission_classes = [IsDoctor]
    queryset = Consultation.objects.select_related("patient", "doctor")


class DoctorConsultationUpdateView(generics.UpdateAPIView):
    serializer_class = ConsultationUpdateSerializer
    permission_classes = [IsDoctor]
    queryset = Consultation.objects.all()

    def perform_update(self, serializer):
        consultation = serializer.save()
        log_audit(
            "record_update",
            self.request.user,
            target=consultation,
            metadata={"fields": list(serializer.validated_data.keys())},
            request=self.request,
        )


@api_view(["POST"])
@permission_classes([IsDoctor])
def doctor_start_consultation(request, queue_id: int):
    try:
        queue_entry = QueueEntry.objects.select_related("patient").get(id=queue_id)
    except QueueEntry.DoesNotExist:
        return Response({"detail": "Fila não encontrada"}, status=404)

    if queue_entry.status == "finished":
        return Response({"detail": "Consulta já finalizada"}, status=400)

    with transaction.atomic():
        consultation = Consultation.objects.create(
            patient=queue_entry.patient,
            doctor=request.user.doctor,
            symptom=queue_entry.symptom,
            status="in_progress",
            room_name=f"{request.user.username}-{queue_entry.patient.id}-{queue_entry.id}",
        )
        queue_entry.status = "in_progress"
        queue_entry.consultation = consultation
        queue_entry.save()
        log_audit("consultation_start", request.user, target=consultation, request=request)
    return Response(ConsultationSerializer(consultation).data)


@api_view(["POST"])
@permission_classes([IsDoctor])
def doctor_finish_consultation(request, consultation_id: int):
    try:
        consultation = Consultation.objects.get(id=consultation_id)
    except Consultation.DoesNotExist:
        return Response({"detail": "Consulta não encontrada"}, status=404)
    consultation.finish()
    if consultation.queue_entry:
        consultation.queue_entry.status = "finished"
        consultation.queue_entry.save()
    log_audit("consultation_finish", request.user, target=consultation, request=request)
    return Response({"status": "finished"})


@api_view(["POST"])
@permission_classes([IsDoctor])
def doctor_generate_document(request, consultation_id: int):
    doc_type = request.data.get("doc_type")
    if doc_type not in dict(Document.TYPE_CHOICES):
        return Response({"detail": "Tipo de documento inválido"}, status=400)
    try:
        consultation = Consultation.objects.select_related("patient", "doctor").get(id=consultation_id)
    except Consultation.DoesNotExist:
        return Response({"detail": "Consulta não encontrada"}, status=404)

    filename, payload = build_document_payload(consultation, doc_type)
    relative_path = generate_pdf(filename, payload.pop("Título"), payload)
    document = Document.objects.create(consultation=consultation, doc_type=doc_type, file=relative_path)

    # envia via WhatsApp
    send_whatsapp_message(
        to_number=consultation.patient.phone,
        body=f"Segue seu documento {doc_type} da Telemed.",
        media_url=None,
    )
    log_audit("pdf_generate", request.user, target=document, metadata={"type": doc_type}, request=request)
    log_audit("document_update", request.user, target=document, metadata={"type": doc_type}, request=request)
    return Response(DocumentSerializer(document).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    if request.user.role == "patient":
        return Response(PatientSerializer(request.user.patient).data)
    if request.user.role == "doctor":
        return Response(DoctorSerializer(request.user.doctor).data)
    return Response({"detail": "Perfil não disponível"}, status=400)


@api_view(["GET"])
@permission_classes([IsDoctor])
def twilio_token(request, consultation_id: int):
    try:
        consultation = Consultation.objects.get(id=consultation_id)
    except Consultation.DoesNotExist:
        return Response({"detail": "Consulta não encontrada"}, status=404)
    room = consultation.room_name or f"{consultation.id}"
    try:
        token = generate_twilio_video_token(identity=str(request.user.username), room=room)
    except ValueError as exc:
        return Response({"detail": str(exc)}, status=400)
    log_audit("video_enter", request.user, target=consultation, metadata={"room": room}, request=request)
    return Response({"token": token, "room": room})


class AuthTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        success = response.status_code == 200
        user = None
        if success and "access" in response.data:
            username = request.data.get("username")
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None
        log_audit("login", user, metadata={"success": success}, success=success, request=request)
        return response


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    refresh = request.data.get("refresh")
    if not refresh:
        return Response({"detail": "Refresh token obrigatório"}, status=400)
    try:
        token = RefreshToken(refresh)
        token.blacklist()
    except Exception:
        log_audit("logout", request.user, metadata={"success": False}, success=False, request=request)
        return Response({"detail": "Token inválido"}, status=400)
    log_audit("logout", request.user, metadata={"success": True}, request=request)
    return Response({"status": "logged_out"})


class PatientUpdateView(generics.UpdateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsPatient]

    def get_object(self):
        return self.request.user.patient

    def perform_update(self, serializer):
        patient = self.get_object()
        old = PatientSerializer(patient).data
        patient = serializer.save()
        new = PatientSerializer(patient).data
        log_audit("update_patient", self.request.user, target=patient, request=self.request, old_value=old, new_value=new)


class DocumentDownloadView(generics.RetrieveAPIView):
    queryset = Document.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        document = self.get_object()
        # simple ownership check
        if request.user.role == "patient" and document.consultation.patient.user != request.user:
            log_audit("unauthorized_access", request.user, target=document, success=False, request=request)
            return Response({"detail": "Sem permissão"}, status=403)
        if request.user.role == "doctor" and document.consultation.doctor and document.consultation.doctor.user != request.user:
            log_audit("unauthorized_access", request.user, target=document, success=False, request=request)
            return Response({"detail": "Sem permissão"}, status=403)
        file_handle = document.file.open("rb")
        log_audit("pdf_download", request.user, target=document, request=request)
        response = FileResponse(file_handle, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{document.file.name.split("/")[-1]}"'
        return response


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def video_exit(request, consultation_id: int):
    try:
        consultation = Consultation.objects.get(id=consultation_id)
    except Consultation.DoesNotExist:
        return Response({"detail": "Consulta não encontrada"}, status=404)
    log_audit("video_exit", request.user, target=consultation, metadata={"room": consultation.room_name}, request=request)
    return Response({"status": "ok"})


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def generate_video_token(request):
    consultation_id = request.data.get("consultation_id")
    if not consultation_id:
        return Response({"detail": "consultation_id obrigatório"}, status=400)
    try:
        consultation = Consultation.objects.get(id=consultation_id)
    except Consultation.DoesNotExist:
        return Response({"detail": "Consulta não encontrada"}, status=404)
    room = consultation.room_name or f"{consultation.id}"
    token = generate_twilio_video_token(identity=str(request.user.username), room=room)
    log_audit("video_enter", request.user, target=consultation, metadata={"room": room}, request=request)
    return Response({"token": token, "room": room})


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def send_document_whatsapp(request):
    document_id = request.data.get("document_id")
    if not document_id:
        return Response({"detail": "document_id obrigatório"}, status=400)
    try:
        document = Document.objects.select_related("consultation__patient").get(id=document_id)
    except Document.DoesNotExist:
        return Response({"detail": "Documento não encontrado"}, status=404)

    # authorization
    if request.user.role == "patient" and document.consultation.patient.user != request.user:
        log_audit("unauthorized_access", request.user, target=document, success=False, request=request)
        return Response({"detail": "Sem permissão"}, status=403)

    patient_phone = document.consultation.patient.phone
    resp = send_whatsapp_message(
        to_number=patient_phone,
        body=f"Documento {document.get_doc_type_display()} da sua consulta.",
        media_url=None,
    )
    log_audit("whatsapp_send", request.user, target=document, metadata=resp, request=request)
    return Response(resp)
