from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [('accounts', '0001_initial')]
    operations = [
        migrations.CreateModel(
            name='DoctorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('crm_number', models.CharField(max_length=50)),
                ('crm_state', models.CharField(max_length=2)),
                ('specialty', models.CharField(max_length=100)),
                ('workload_hours', models.PositiveIntegerField(default=0)),
                ('digital_signature', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctorprofile', to='accounts.user')),
            ],
        ),
    ]
