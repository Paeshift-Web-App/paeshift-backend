# Generated by Django 5.1.7 on 2025-03-22 19:07

import notifications.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("notifications", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notificationpreference",
            name="email_preferences",
            field=models.JSONField(
                default=notifications.models.default_email_preferences
            ),
        ),
        migrations.AlterField(
            model_name="notificationpreference",
            name="push_preferences",
            field=models.JSONField(
                default=notifications.models.default_push_preferences
            ),
        ),
    ]
