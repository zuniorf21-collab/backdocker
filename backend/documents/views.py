import time
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from consultations.models import Consultation, MedicalRecordEntry
from documents.models import DocumentRecord
from documents.serializers import (
    AtestadoSerializer,
    DeclaracaoAcompanhamentoSerializer,
    DeclaracaoComparecimentoSerializer,
    PrescricaoSerializer,
)
from documents.utils import generate_pdf, generate_qr_code


def _ensure_doctor_access(request, consultation):
    if not consultation.doctor or consultation.doctor.user != request.user:
        return False
    return True


def _save_record(consultation, doc_type, pdf_io, filename):
    record = DocumentRecord(consultation=consultation, type=doc_type)
    record.file.save(filename, ContentFile(pdf_io.getvalue()), save=True)
    return record


def _create_prontuario_entry(user, consultation, doc_type, record):
    MedicalRecordEntry.objects.create(
        patient=consultation.patient,
        consultation=consultation,
        author=user,
        entry_type="note",
        content=f"Documento emitido: {doc_type}",
        attachments=[{"file": record.file.url}],
    )


class AtestadoView(APIView):
    def post(self, request, consultation_id):
        consultation = get_object_or_404(Consultation, pk=consultation_id)
        if not _ensure_doctor_access(request, consultation):
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        serializer = AtestadoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        context = {
            **serializer.validated_data,
            "doctor": consultation.doctor,
            "consultation": consultation,
            "qr_code_path": generate_qr_code(f"https://telemed.local/documents/{consultation_id}/atestado"),
            "logo_path": "/app/static/logo.png",
            "title": "Atestado Médico",
            "primary_color": "#0C6DFD",
        }
        pdf_io = generate_pdf("documents/atestado.html", context)
        filename = f"atestado_{consultation_id}_{int(time.time())}.pdf"
        record = _save_record(consultation, DocumentRecord.TYPE_ATESTADO, pdf_io, filename)
        _create_prontuario_entry(request.user, consultation, "atestado", record)

        response = HttpResponse(pdf_io.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class DeclaracaoAcompanhamentoView(APIView):
    def post(self, request, consultation_id):
        consultation = get_object_or_404(Consultation, pk=consultation_id)
        if not _ensure_doctor_access(request, consultation):
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        serializer = DeclaracaoAcompanhamentoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        context = {
            **serializer.validated_data,
            "doctor": consultation.doctor,
            "consultation": consultation,
            "qr_code_path": generate_qr_code(f"https://telemed.local/documents/{consultation_id}/declaracao-acompanhamento"),
            "logo_path": "/app/static/logo.png",
            "title": "Declaração de Acompanhamento",
            "primary_color": "#0C6DFD",
        }
        pdf_io = generate_pdf("documents/declaracao_acompanhamento.html", context)
        filename = f"declaracao_acompanhamento_{consultation_id}_{int(time.time())}.pdf"
        record = _save_record(consultation, DocumentRecord.TYPE_ACOMPANHAMENTO, pdf_io, filename)
        _create_prontuario_entry(request.user, consultation, "declaracao_acompanhamento", record)

        response = HttpResponse(pdf_io.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class DeclaracaoComparecimentoView(APIView):
    def post(self, request, consultation_id):
        consultation = get_object_or_404(Consultation, pk=consultation_id)
        if not _ensure_doctor_access(request, consultation):
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        serializer = DeclaracaoComparecimentoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        context = {
            **serializer.validated_data,
            "doctor": consultation.doctor,
            "consultation": consultation,
            "qr_code_path": generate_qr_code(f"https://telemed.local/documents/{consultation_id}/declaracao-comparecimento"),
            "logo_path": "/app/static/logo.png",
            "title": "Declaração de Comparecimento",
            "primary_color": "#0C6DFD",
        }
        pdf_io = generate_pdf("documents/declaracao_comparecimento.html", context)
        filename = f"declaracao_comparecimento_{consultation_id}_{int(time.time())}.pdf"
        record = _save_record(consultation, DocumentRecord.TYPE_COMPARECIMENTO, pdf_io, filename)
        _create_prontuario_entry(request.user, consultation, "declaracao_comparecimento", record)

        response = HttpResponse(pdf_io.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class PrescricaoView(APIView):
    def post(self, request, consultation_id):
        consultation = get_object_or_404(Consultation, pk=consultation_id)
        if not _ensure_doctor_access(request, consultation):
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        serializer = PrescricaoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        context = {
            **serializer.validated_data,
            "doctor": consultation.doctor,
            "consultation": consultation,
            "qr_code_path": generate_qr_code(f"https://telemed.local/documents/{consultation_id}/prescricao"),
            "logo_path": "/app/static/logo.png",
            "title": "Prescrição Médica",
            "primary_color": "#0C6DFD",
        }
        pdf_io = generate_pdf("documents/prescricao.html", context)
        filename = f"prescricao_{consultation_id}_{int(time.time())}.pdf"
        record = _save_record(consultation, DocumentRecord.TYPE_PRESCRICAO, pdf_io, filename)
        _create_prontuario_entry(request.user, consultation, "prescricao", record)

        response = HttpResponse(pdf_io.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
