from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_auditlog"),
    ]

    operations = [
        migrations.AddField(
            model_name="auditlog",
            name="new_value",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="auditlog",
            name="old_value",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
