from ninja import Router
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.db import transaction
from .models import *
from jobs.models import User

router = Router(tags=["Notifications"])


# ✅ Helper function to get authenticated user
def get_authenticated_user(request):
    """Retrieve the authenticated user from session."""
    user_id = request.session.get("_auth_user_id")
    if not user_id:
        return None
    return get_object_or_404(User, id=user_id)


# ✅ Get All Notifications
@router.get("/notifications/")
def get_notifications(request):
    """Retrieve all notifications for the authenticated user."""
    user = get_authenticated_user(request)
    if not user:
        return JsonResponse({"error": "User not authenticated"}, status=403)

    notifications = Notification.objects.filter(user=user).order_by("-created_at")
    
    return JsonResponse([
        {
            "id": n.id,
            "message": n.message,
            "category": n.category,
            "is_read": n.is_read,
            "created_at": n.created_at
        }
        for n in notifications
    ], safe=False)


# ✅ Mark Notification as Read
@router.post("/notifications/{notification_id}/mark-as-read/")
def mark_notification_as_read(request, notification_id: int):
    """Mark a specific notification as read."""
    user = get_authenticated_user(request)
    if not user:
        return JsonResponse({"error": "User not authenticated"}, status=403)

    notification = get_object_or_404(Notification, id=notification_id, user=user)
    notification.is_read = True
    notification.save()

    return JsonResponse({"status": "Notification marked as read"})


# ✅ Get Notification Preferences
@router.get("/notifications/settings")
def get_notification_settings(request):
    """Retrieve the notification settings for the authenticated user."""
    user = get_authenticated_user(request)
    if not user:
        return JsonResponse({"error": "User not authenticated"}, status=403)

    settings, _ = NotificationPreference.objects.get_or_create(user=user)

    return JsonResponse({
        "push": settings.push_preferences,
        "email": settings.email_preferences
    })


# ✅ Update Notification Preferences
@router.put("/notifications/settings")
def update_notification_settings(request, preference_type: str, category: str, value: bool):
    """
    Update notification preferences dynamically.

    :param preference_type: "push" or "email"
    :param category: Notification category (e.g., "new_job_alert")
    :param value: True (enable) or False (disable)
    """
    user = get_authenticated_user(request)
    if not user:
        return JsonResponse({"error": "User not authenticated"}, status=403)

    settings, _ = NotificationPreference.objects.get_or_create(user=user)

    # Update based on preference type
    if preference_type == "push":
        settings.push_preferences[category] = value
    elif preference_type == "email":
        settings.email_preferences[category] = value
    else:
        return JsonResponse({"error": "Invalid preference type"}, status=400)

    settings.save()
    return JsonResponse({"message": "Notification settings updated successfully"})


# ✅ Send Notifications (Push & Email)
def send_notification(user, category, message):
    """Send push/email notifications based on user preferences."""
    settings = NotificationPreference.objects.filter(user=user).first()

    if not settings:
        return  # No settings available

    # Determine if push or email should be sent
    send_push = settings.push_preferences.get(category, False)
    send_email = settings.email_preferences.get(category, False)

    # Send push notification (implement your push service here)
    if send_push:
        print(f"🔔 Push notification sent to {user.username}: {message}")

    # Send email notification
    if send_email:
        send_mail(
            subject=f"{category.replace('_', ' ').title()} Notification",
            message=message,
            from_email="noreply@yourapp.com",
            recipient_list=[user.email],
        )

    # Save the notification in DB
    Notification.objects.create(user=user, category=category, message=message)

    return {"push_sent": send_push, "email_sent": send_email}
