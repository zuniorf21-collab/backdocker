from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [('patients', '0001_initial'), ('doctors', '0001_initial'), ('payments', '0001_initial')]
    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pendente'), ('waiting', 'Fila'), ('active', 'Em atendimento'), ('completed', 'Concluida'), ('cancelled', 'Cancelada')], default='pending', max_length=20)),
                ('scheduled_at', models.DateTimeField(blank=True, null=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('twilio_room_name', models.CharField(blank=True, max_length=120)),
                ('twilio_token', models.CharField(blank=True, max_length=255)),
                ('recording_url', models.URLField(blank=True)),
                ('diagnosis', models.TextField(blank=True)),
                ('cid10', models.CharField(blank=True, max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultations', to='doctors.doctorprofile')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultations', to='patients.patientprofile')),
                ('payment', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultation', to='payments.payment')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalRecordEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_type', models.CharField(choices=[('note', 'Evolucao'), ('diagnosis', 'Diagnostico'), ('prescription', 'Receita'), ('certificate', 'Atestado')], max_length=20)),
                ('content', models.TextField()),
                ('cid10', models.CharField(blank=True, max_length=20)),
                ('attachments', models.JSONField(blank=True, default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.user')),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='consultations.consultation')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='patients.patientprofile')),
            ],
            options={'ordering': ['created_at']},
        ),
    ]
