from ninja import Schema

class NotificationSettingsSchema(Schema):
    push_new_job_alert: bool
    push_job_reminder: bool
    push_job_acceptance: bool
    push_settings_changes: bool
    email_new_job_alert: bool
    email_job_reminder: bool
    email_job_acceptance: bool
    email_settings_changes: bool
