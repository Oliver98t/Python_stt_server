# Generated by Django 5.2.3 on 2025-06-21 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_delete_snippet'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcription',
            name='ip',
            field=models.CharField(blank=True, null=True),
        ),
    ]
