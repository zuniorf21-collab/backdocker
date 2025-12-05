from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("consultations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DocumentRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("type", models.CharField(choices=[("atestado", "Atestado"), ("declaracao_acompanhamento", "Declaracao de Acompanhamento"), ("declaracao_comparecimento", "Declaracao de Comparecimento"), ("prescricao", "Prescricao")], max_length=30)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("file", models.FileField(upload_to="documents/")),
                ("consultation", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="consultations.consultation")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
