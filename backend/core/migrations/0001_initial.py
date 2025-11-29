from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                ("is_superuser", models.BooleanField(default=False, help_text="Designates that this user has all permissions without explicitly assigning them.", verbose_name="superuser status")),
                ("username", models.CharField(max_length=150, unique=True, verbose_name="username")),
                ("first_name", models.CharField(blank=True, max_length=150, verbose_name="first name")),
                ("last_name", models.CharField(blank=True, max_length=150, verbose_name="last name")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="email address")),
                ("is_staff", models.BooleanField(default=False, help_text="Designates whether the user can log into this admin site.", verbose_name="staff status")),
                ("is_active", models.BooleanField(default=True, help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.", verbose_name="active")),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
                ("role", models.CharField(choices=[("patient", "Paciente"), ("doctor", "Médico"), ("admin", "Admin")], default="patient", max_length=20)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("groups", models.ManyToManyField(blank=True, help_text="The groups this user belongs to.", related_name="user_set", related_query_name="user", to="auth.group", verbose_name="groups")),
                ("user_permissions", models.ManyToManyField(blank=True, help_text="Specific permissions for this user.", related_name="user_set", related_query_name="user", to="auth.permission", verbose_name="user permissions")),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Doctor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=255)),
                ("crm", models.CharField(max_length=50)),
                ("specialty", models.CharField(blank=True, max_length=100)),
                ("digital_signature", models.CharField(blank=True, max_length=255)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="doctor", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=255)),
                ("cpf", models.CharField(max_length=14, unique=True)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=20)),
                ("birth_date", models.DateField()),
                ("address", models.TextField()),
                ("symptom_initial", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="patient", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Consultation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("symptom", models.TextField()),
                ("anamnesis", models.TextField(blank=True)),
                ("notes", models.TextField(blank=True)),
                ("prescription", models.TextField(blank=True)),
                ("certificate", models.TextField(blank=True)),
                ("declaration", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("scheduled", "Agendada"), ("in_progress", "Em andamento"), ("finished", "Finalizada")], default="scheduled", max_length=20)),
                ("room_name", models.CharField(blank=True, max_length=100)),
                ("started_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                ("doctor", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="consultations", to="core.doctor")),
                ("patient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="consultations", to="core.patient")),
            ],
        ),
        migrations.CreateModel(
            name="QueueEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("symptom", models.TextField()),
                ("status", models.CharField(choices=[("waiting", "Esperando"), ("in_progress", "Atendendo"), ("finished", "Finalizado")], default="waiting", max_length=20)),
                ("consultation", models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="queue_entry", to="core.consultation")),
                ("patient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="queue_entries", to="core.patient")),
            ],
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("doc_type", models.CharField(choices=[("anamnesis", "Anamnese"), ("prescription", "Receita"), ("certificate", "Atestado"), ("declaration", "Declaração")], max_length=20)),
                ("file", models.FileField(upload_to="documents/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("consultation", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="documents", to="core.consultation")),
            ],
        ),
    ]
