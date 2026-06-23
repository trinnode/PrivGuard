from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0003_incident_anonymize_requested'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='status',
            field=models.CharField(
                choices=[
                    ('draft', 'Draft'),
                    ('submitted', 'Submitted'),
                    ('under_review', 'Under Review'),
                    ('resolved', 'Resolved'),
                    ('closed', 'Closed'),
                ],
                default='submitted',
                max_length=20,
                verbose_name='Incident Status',
            ),
        ),
    ]
