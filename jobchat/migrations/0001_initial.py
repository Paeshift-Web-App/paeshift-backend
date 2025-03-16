# Generated by Django 5.1.7 on 2025-03-16 09:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("jobs", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="LocationHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("latitude", models.FloatField(verbose_name="Latitude")),
                ("longitude", models.FloatField(verbose_name="Longitude")),
                (
                    "address",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Address"
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="locations",
                        to="jobs.job",
                        verbose_name="Job",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="location_histories",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Location History",
                "verbose_name_plural": "Location Histories",
                "ordering": ["-timestamp"],
                "indexes": [
                    models.Index(
                        fields=["-timestamp"], name="jobchat_loc_timesta_901595_idx"
                    ),
                    models.Index(fields=["job"], name="jobchat_loc_job_id_9b3547_idx"),
                    models.Index(
                        fields=["user", "latitude", "longitude"],
                        name="jobchat_loc_user_id_a36f45_idx",
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField(verbose_name="Message Content")),
                (
                    "timestamp",
                    models.DateTimeField(auto_now_add=True, verbose_name="Sent At"),
                ),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="jobs.job",
                        verbose_name="Related Job",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_messages",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Sender",
                    ),
                ),
            ],
            options={
                "verbose_name": "Chat Message",
                "verbose_name_plural": "Chat Messages",
                "ordering": ["-timestamp"],
                "indexes": [
                    models.Index(
                        fields=["-timestamp"], name="jobchat_mes_timesta_7f1286_idx"
                    ),
                    models.Index(fields=["job"], name="jobchat_mes_job_id_a2efa0_idx"),
                ],
            },
        ),
    ]
