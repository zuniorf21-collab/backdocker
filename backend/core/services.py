import os
from pathlib import Path
from datetime import datetime
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from twilio.rest import Client
from .audit import log_audit


def ensure_media_dir() -> Path:
    media = Path(settings.MEDIA_ROOT)
    media.mkdir(parents=True, exist_ok=True)
    docs = media / "documents"
    docs.mkdir(parents=True, exist_ok=True)
    return docs


def generate_pdf(filename: str, title: str, content: dict) -> str:
    docs_dir = ensure_media_dir()
    filepath = docs_dir / filename
    c = canvas.Canvas(str(filepath), pagesize=A4)
    width, height = A4
    c.setTitle(title)

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, title)
    y -= 30

    c.setFont("Helvetica", 11)
    for label, value in content.items():
        c.drawString(50, y, f"{label}: {value}")
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)

    c.showPage()
    c.save()
    return str(filepath.relative_to(settings.MEDIA_ROOT))


def generate_twilio_video_token(identity: str, room: str) -> str:
    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY_SID
    api_secret = settings.TWILIO_API_KEY_SECRET
    if not all([account_sid, api_key, api_secret]):
        raise ValueError("Twilio credentials are not configured.")

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)
    video_grant = VideoGrant(room=room)
    token.add_grant(video_grant)
    return token.to_jwt().decode("utf-8")


def send_whatsapp_message(to_number: str, body: str, media_url: str | None = None) -> dict:
    provider = getattr(settings, "WHATSAPP_PROVIDER", "twilio")
    if provider != "twilio":
        return {"status": "skipped", "reason": "Unsupported provider"}

    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_API_KEY_SECRET or os.environ.get("TWILIO_AUTH_TOKEN")
    whatsapp_from = settings.TWILIO_WHATSAPP_FROM
    if not all([account_sid, auth_token, whatsapp_from]):
        return {"status": "skipped", "reason": "Missing Twilio WhatsApp credentials"}

    client = Client(account_sid, auth_token)
    params = {"from_": f"whatsapp:{whatsapp_from}", "to": f"whatsapp:{to_number}", "body": body}
    if media_url:
        params["media_url"] = [media_url]
    message = client.messages.create(**params)
    log_audit("whatsapp_send", None, metadata={"to": to_number, "media_url": media_url, "sid": message.sid})
    return {"status": "sent", "sid": message.sid}


def build_document_payload(consultation, doc_type: str) -> tuple[str, dict]:
    title_map = {
        "anamnesis": "Anamnese",
        "prescription": "Receita",
        "certificate": "Atestado",
        "declaration": "Declaração",
    }
    title = title_map.get(doc_type, "Documento")
    filename = f"{doc_type}-{consultation.id}-{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    patient = consultation.patient
    doctor = consultation.doctor
    content = {
        "Paciente": patient.full_name,
        "CPF": patient.cpf,
        "Telefone": patient.phone,
        "Médico": doctor.full_name if doctor else "",
        "CRM": doctor.crm if doctor else "",
        "Horário": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Assinatura": doctor.digital_signature if doctor else "Assinatura padrão",
        "Conteúdo": getattr(consultation, doc_type, ""),
    }
    return filename, {"Título": title, **content}
