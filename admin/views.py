from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.core.serializers import serialize
import json
from .models import Job, Dispute, Payment, AdminRole
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
User = get_user_model()



def admin_signup(request):
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('finance', 'Finance Admin'),
        ('support', 'Support Admin'),
        ('moderator', 'Moderator'),
    ]

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")  # Get selected role from the form

        if not role in dict(ROLE_CHOICES):
            messages.error(request, "Invalid role selected.")
            return redirect("admin_signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            # Create a superuser (admin)
            user = User.objects.create_superuser(username=username, password=password)
            
            # Assign role
            AdminRole.objects.create(user=user, role=role)

            # Log in the admin user
            login(request, user)
            return redirect("admin_dashboard")

    return render(request, "admin_signup.html", {"roles": ROLE_CHOICES})


# ==============================
# 1. User Management
# ==============================

def get_all_users(request):
    """
    GET /admin/users
    Fetches a list of all users in the system.
    """
    users = User.objects.all()
    users_data = serialize('json', users, fields=('username', 'email', 'role', 'is_active', 'date_joined'))
    return JsonResponse(users_data, safe=False)


def get_user_by_id(request, user_id):
    """
    GET /admin/users/{user_id}
    Fetches detailed information about a specific user.
    """
    user = get_object_or_404(User, id=user_id)
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "profile": {
            "first_name": user.profile.first_name,
            "last_name": user.profile.last_name,
            "profile_pic_url": user.profile.profile_pic_url
        },
        "ratings": list(user.ratings_received.values('rating', 'feedback')),
        "jobs_posted": user.jobs_posted.count(),
        "jobs_applied": user.jobs_applied.count()
    }
    return JsonResponse(user_data)


@require_http_methods(["PUT"])
def activate_user(request, user_id):
    """
    PUT /admin/users/{user_id}/activate
    Activates or deactivates a user account.
    """
    user = get_object_or_404(User, id=user_id)
    data = json.loads(request.body)
    user.is_active = data.get('is_active', user.is_active)
    user.save()
    return JsonResponse({"message": f"User {'activated' if user.is_active else 'deactivated'} successfully"})


@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    """
    DELETE /admin/users/{user_id}
    Deletes a user account from the system.
    """
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return JsonResponse({"message": "User deleted successfully"})


# ==============================
# 2. Job Management
# ==============================

def get_all_jobs(request):
    """
    GET /admin/jobs
    Fetches a list of all jobs in the system.
    """
    jobs = Job.objects.all()
    jobs_data = list(jobs.values('id', 'title', 'client__username', 'status', 'date', 'start_time', 'end_time', 'location', 'rate'))
    return JsonResponse(jobs_data, safe=False)


def get_job_by_id(request, job_id):
    """
    GET /admin/jobs/{job_id}
    Fetches detailed information about a specific job.
    """
    job = get_object_or_404(Job, id=job_id)
    job_data = {
        "id": job.id,
        "title": job.title,
        "client": job.client.username,
        "status": job.status,
        "date": job.date,
        "start_time": job.start_time,
        "end_time": job.end_time,
        "location": job.location,
        "rate": job.rate,
        "applicants": list(job.applicants.values('username', 'email')),
        "disputes": list(job.disputes.values('title', 'description', 'status'))
    }
    return JsonResponse(job_data)


@require_http_methods(["PUT"])
def update_job_status(request, job_id):
    """
    PUT /admin/jobs/{job_id}/status
    Updates the status of a job.
    """
    job = get_object_or_404(Job, id=job_id)
    data = json.loads(request.body)
    job.status = data.get('status', job.status)
    job.save()
    return JsonResponse({"message": f"Job status updated to {job.status}"})


@require_http_methods(["DELETE"])
def delete_job(request, job_id):
    """
    DELETE /admin/jobs/{job_id}
    Deletes a job from the system.
    """
    job = get_object_or_404(Job, id=job_id)
    job.delete()
    return JsonResponse({"message": "Job deleted successfully"})


# ==============================
# 3. Dispute Management
# ==============================

def get_all_disputes(request):
    """
    GET /admin/disputes
    Fetches a list of all disputes in the system.
    """
    disputes = Dispute.objects.all()
    disputes_data = list(disputes.values('id', 'title', 'description', 'status', 'created_by__username', 'created_at', 'job__title'))
    return JsonResponse(disputes_data, safe=False)


def get_dispute_by_id(request, dispute_id):
    """
    GET /admin/disputes/{dispute_id}
    Fetches detailed information about a specific dispute.
    """
    dispute = get_object_or_404(Dispute, id=dispute_id)
    dispute_data = {
        "id": dispute.id,
        "title": dispute.title,
        "description": dispute.description,
        "status": dispute.status,
        "created_by": dispute.created_by.username,
        "created_at": dispute.created_at,
        "job": dispute.job.title,
        "messages": list(dispute.messages.values('sender__username', 'message', 'timestamp'))
    }
    return JsonResponse(dispute_data)


@require_http_methods(["PUT"])
def resolve_dispute(request, dispute_id):
    """
    PUT /admin/disputes/{dispute_id}/resolve
    Resolves a dispute by updating its status.
    """
    dispute = get_object_or_404(Dispute, id=dispute_id)
    data = json.loads(request.body)
    dispute.status = data.get('status', dispute.status)
    dispute.save()
    return JsonResponse({"message": f"Dispute resolved with status: {dispute.status}"})


@require_http_methods(["DELETE"])
def delete_dispute(request, dispute_id):
    """
    DELETE /admin/disputes/{dispute_id}
    Deletes a dispute from the system.
    """
    dispute = get_object_or_404(Dispute, id=dispute_id)
    dispute.delete()
    return JsonResponse({"message": "Dispute deleted successfully"})


# ==============================
# 4. Payment Management
# ==============================

def get_all_payments(request):
    """
    GET /admin/payments
    Fetches a list of all payments in the system.
    """
    payments = Payment.objects.all()
    payments_data = list(payments.values('id', 'payer__username', 'recipient__username', 'job__title', 'amount', 'status', 'created_at'))
    return JsonResponse(payments_data, safe=False)


def get_payment_by_id(request, payment_id):
    """
    GET /admin/payments/{payment_id}
    Fetches detailed information about a specific payment.
    """
    payment = get_object_or_404(Payment, id=payment_id)
    payment_data = {
        "id": payment.id,
        "payer": payment.payer.username,
        "recipient": payment.recipient.username,
        "job": payment.job.title,
        "amount": payment.amount,
        "status": payment.status,
        "created_at": payment.created_at
    }
    return JsonResponse(payment_data)


@require_http_methods(["PUT"])
def update_payment_status(request, payment_id):
    """
    PUT /admin/payments/{payment_id}/status
    Updates the status of a payment.
    """
    payment = get_object_or_404(Payment, id=payment_id)
    data = json.loads(request.body)
    payment.status = data.get('status', payment.status)
    payment.save()
    return JsonResponse({"message": f"Payment status updated to {payment.status}"})


@require_http_methods(["DELETE"])
def delete_payment(request, payment_id):
    """
    DELETE /admin/payments/{payment_id}
    Deletes a payment from the system.
    """
    payment = get_object_or_404(Payment, id=payment_id)
    payment.delete()
    return JsonResponse({"message": "Payment deleted successfully"})


# ==============================
# 5. Analytics & Reports
# ==============================

def generate_analytics_report(request):
    """
    GET /admin/analytics
    Generates a system-wide analytics report.
    """
    total_users = User.objects.count()
    total_jobs = Job.objects.count()
    total_payments = Payment.objects.count()
    total_disputes = Dispute.objects.count()

    report = {
        "total_users": total_users,
        "total_jobs": total_jobs,
        "total_payments": total_payments,
        "total_disputes": total_disputes
    }
    return JsonResponse(report)