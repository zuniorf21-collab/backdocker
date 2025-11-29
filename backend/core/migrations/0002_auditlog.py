from django.db import migrations, models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("action", models.CharField(choices=[("login", "Login"), ("logout", "Logout"), ("create_patient", "Criação de paciente"), ("update_patient", "Alteração de dados"), ("queue_enter", "Entrada na fila"), ("consultation_start", "Início de consulta"), ("consultation_finish", "Fim de consulta"), ("pdf_generate", "Geração de PDF"), ("pdf_download", "Download de PDF"), ("whatsapp_send", "Envio pelo WhatsApp"), ("unauthorized_access", "Tentativa de acesso indevido"), ("record_update", "Alterações de prontuário"), ("document_update", "Alterações de documentos"), ("video_enter", "Entrada na sala de vídeo"), ("video_exit", "Saída da sala de vídeo")], max_length=50)),
                ("target_type", models.CharField(blank=True, max_length=100)),
                ("target_id", models.CharField(blank=True, max_length=100)),
                ("ip", models.GenericIPAddressField(blank=True, null=True)),
                ("success", models.BooleanField(default=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
