from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [('consultations', '0001_initial'), ('patients', '0001_initial')]
    operations = [
        migrations.CreateModel(
            name='QueueEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('waiting', 'Aguardando'), ('served', 'Atendido'), ('cancelled', 'Cancelado')], default='waiting', max_length=20)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('served_at', models.DateTimeField(blank=True, null=True)),
                ('consultation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='queue_entry', to='consultations.consultation')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queue_entries', to='patients.patientprofile')),
            ],
            options={'ordering': ['joined_at']},
        ),
    ]
