from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [('patients', '0001_initial'), ('doctors', '0001_initial'), ('consultations', '0001_initial')]
    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('pdf_content', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='consultations.consultation')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='doctors.doctorprofile')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='patients.patientprofile')),
            ],
        ),
    ]
