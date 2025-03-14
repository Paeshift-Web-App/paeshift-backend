from math import radians, sin, cos, sqrt, atan2
from django.db.models import Avg, Count
from jobs.models import Job, Application
from django.contrib.auth import get_user_model

User = get_user_model()

# Haversine function to calculate distances (Earth radius ~6371 km)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Distance in km

# Find best applicants without GIS
def find_best_applicants(job, max_distance_km=50):
    if not job.latitude or not job.longitude:
        return []  # Ensure the job has a valid location

    applicants = (
        Application.objects.filter(job=job, status="pending")
        .select_related("user__profile")
        .annotate(avg_rating=Avg("user__profile__rating"))
    )

    filtered_applicants = []
    for applicant in applicants:
        user = applicant.user
        if user.profile.latitude and user.profile.longitude:
            distance = haversine(job.latitude, job.longitude, user.profile.latitude, user.profile.longitude)
            if distance <= max_distance_km:
                filtered_applicants.append({"user": user, "distance": distance, "rating": applicant.avg_rating or 0})

    # Sort: highest rating first, nearest second
    return sorted(filtered_applicants, key=lambda x: (-x["rating"], x["distance"]))[:10]
