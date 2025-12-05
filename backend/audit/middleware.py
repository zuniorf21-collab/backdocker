import json
import os
from django.conf import settings
from django.utils import timezone
from audit.models import AuditLog
from utils.validators import mask_payload


class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            user = request.user if request.user.is_authenticated else None
            payload = {}
            should_log_body = settings.DEBUG or os.environ.get("AUDIT_LOG_BODY", "0") == "1"
            if should_log_body and request.body:
                try:
                    payload = json.loads(request.body.decode('utf-8'))
                except Exception:
                    payload = {}
            AuditLog.objects.create(
                user=user,
                path=request.path,
                method=request.method,
                ip_address=request.META.get('REMOTE_ADDR'),
                payload=mask_payload(payload),
                created_at=timezone.now(),
            )
        except Exception:
            pass
        return response
