# Generated by Django 5.1.6 on 2025-03-09 08:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0007_remove_job_applicants_remove_job_is_deleted_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="job_type",
            field=models.CharField(
                choices=[("single_day", "Single Day"), ("multiple_days", "Weekly")],
                default="single_day",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="role",
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
