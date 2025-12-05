from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from payments.models import Payment
from payments.serializers import PaymentSerializer, PaymentProcessSerializer
from accounts.permissions import IsAdmin, IsPatient


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        base_qs = Payment.objects.all().select_related('patient')
        if getattr(user, "role", None) == user.Role.ADMIN or getattr(user, "is_superuser", False):
            return base_qs
        if hasattr(user, "patientprofile"):
            return base_qs.filter(patient=user.patientprofile)
        return base_qs.none()

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated(), IsPatient()]
        elif self.action in ['process']:
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        if not hasattr(self.request.user, "patientprofile"):
            raise PermissionDenied("Somente pacientes podem criar pagamentos.")
        serializer.save(patient=self.request.user.patientprofile)

    @action(detail=True, methods=['post'], url_path='process')
    def process(self, request, pk=None):
        payment = self.get_object()
        if payment.status != Payment.STATUS_PENDING:
            return Response({"detail": "Pagamento ja processado."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PaymentProcessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(payment, serializer.validated_data)
        return Response(PaymentSerializer(payment).data)
