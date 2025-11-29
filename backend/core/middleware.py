from django.utils.deprecation import MiddlewareMixin
from .audit import log_audit


class AuditMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # log only authenticated write operations
        if request.method in ["POST", "PUT", "PATCH", "DELETE"] and request.user.is_authenticated:
            log_audit(
                action="record_update",
                user=request.user,
                metadata={"path": request.path, "method": request.method},
                request=request,
            )
        return None
