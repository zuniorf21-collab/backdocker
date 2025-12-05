from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from payments.views import PaymentViewSet
from prescriptions.views import PrescriptionViewSet
from certificates.views import CertificateViewSet
from consultations.views import ConsultationStartView, ConsultationEndView, ConsultationListCreateView, MedicalRecordEntryViewSet
from queueapp.views import QueueJoinView, QueueNextView
from accounts.views import AdminUserCreateView, MeView, PatientRegistrationView
from doctors.views import DoctorCreateView, DoctorListView
from django.urls import include

router = routers.DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')
router.register(r'certificates', CertificateViewSet, basename='certificate')

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('patients/register/', PatientRegistrationView.as_view(), name='patient-register'),
    path('patients/me/', MeView.as_view(), name='patient-me'),
    path('admin/users/', AdminUserCreateView.as_view(), name='admin-user-create'),
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/create/', DoctorCreateView.as_view(), name='doctor-create'),
    path('consultations/', ConsultationListCreateView.as_view(), name='consultation-list-create'),
    path('consultations/<int:pk>/start/', ConsultationStartView.as_view(), name='consultation-start'),
    path('consultations/<int:pk>/end/', ConsultationEndView.as_view(), name='consultation-end'),
    path('records/', MedicalRecordEntryViewSet.as_view(), name='records'),
    path('queue/join/', QueueJoinView.as_view(), name='queue-join'),
    path('queue/next/', QueueNextView.as_view(), name='queue-next'),
    path('documents/', include('documents.urls')),
    path('', include(router.urls)),
]
