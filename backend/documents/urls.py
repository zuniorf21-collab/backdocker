from django.urls import path
from documents import views

urlpatterns = [
    path("atestado/<int:consultation_id>/", views.AtestadoView.as_view(), name="document-atestado"),
    path("declaracao-acompanhamento/<int:consultation_id>/", views.DeclaracaoAcompanhamentoView.as_view(), name="document-declaracao-acompanhamento"),
    path("declaracao-comparecimento/<int:consultation_id>/", views.DeclaracaoComparecimentoView.as_view(), name="document-declaracao-comparecimento"),
    path("prescricao/<int:consultation_id>/", views.PrescricaoView.as_view(), name="document-prescricao"),
]
