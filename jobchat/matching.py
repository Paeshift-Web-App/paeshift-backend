import django
django.setup()  # Ensure Django is fully initialized

from django.db.models import Avg, Count, Q
from django.apps import apps
from django.contrib.auth import get_user_model
from math import radians, sin, cos, sqrt, atan2

# Lazy-load models
Job = apps.get_model("jobs", "Job")
Application = apps.get_model("jobs", "Application", "UserLocation")
User = get_user_model()

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two latitude/longitude points using Haversine formula.
    """
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Distance in km

def find_best_applicants(job, max_distance_km=50):
    """Finds best applicants for a job based on rating & location."""
    job_lat, job_lon = job.latitude, job.longitude
    if not job_lat or not job_lon:
        return []

    applicants = (
        Application.objects.filter(job=job, status="pending")
        .select_related("user__profile", "user__location")
        .annotate(
            avg_rating=Avg("user__profile__rating"),
            total_jobs=Count("user__accepted_jobs"),
        )
    )

    filtered_applicants = []
    for applicant in applicants:
        user_loc = applicant.user.location
        if user_loc and user_loc.latitude and user_loc.longitude:
            distance = haversine(job_lat, job_lon, user_loc.latitude, user_loc.longitude)
            if distance <= max_distance_km:
                filtered_applicants.append((applicant, distance))

    sorted_applicants = sorted(filtered_applicants, key=lambda x: (x[1], -x[0].avg_rating))
    return [applicant[0] for applicant in sorted_applicants]
