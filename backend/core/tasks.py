from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail

@shared_task
def send_async_email(subject: str, message: str, recipient_list: list[str]):
    send_mail(subject, message, 'no-reply@telemed.local', recipient_list)

@shared_task
def cleanup_expired_tokens():
    return {'ran_at': timezone.now().isoformat()}

@shared_task
def log_audit_event(payload: dict):
    return payload
