from __future__ import annotations

from typing import Any, Optional
from django.contrib.auth import get_user_model
from rest_framework.views import exception_handler
from .models import AuditLog


def get_client_ip(request) -> Optional[str]:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def log_audit(
    action: str,
    user: Optional[User],
    target: Optional[Any] = None,
    metadata: Optional[dict] = None,
    success: bool = True,
    request=None,
    old_value: Optional[dict] = None,
    new_value: Optional[dict] = None,
):
    target_type = target.__class__.__name__ if target is not None else ""
    target_id = getattr(target, "id", "") if target is not None else ""
    ip = get_client_ip(request) if request else None
    AuditLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action=action,
        target_type=target_type,
        target_id=str(target_id),
        ip=ip,
        success=success,
        metadata=metadata or {},
        old_value=old_value,
        new_value=new_value,
    )


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    request = context.get("request")
    if response and response.status_code in (401, 403):
        log_audit(
            action="unauthorized_access",
            user=request.user if request else None,
            target=None,
            metadata={"path": request.path if request else "", "method": request.method if request else ""},
            success=False,
            request=request,
        )
    return response
