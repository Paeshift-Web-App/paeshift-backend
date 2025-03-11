# Generated by Django 5.1.6 on 2025-03-11 12:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0013_job_pay_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="role",
            field=models.CharField(
                blank=True,
                choices=[
                    ("applicant", "Applicant"),
                    ("client", "Client"),
                    ("admin", "Admin"),
                ],
                max_length=20,
            ),
        ),
    ]
