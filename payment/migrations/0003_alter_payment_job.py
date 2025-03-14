# Generated by Django 5.1.6 on 2025-03-14 17:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0004_alter_application_options_alter_job_options_and_more"),
        ("payment", "0002_alter_payment_options_alter_wallet_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="job",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payments",
                to="jobs.job",
            ),
        ),
    ]
