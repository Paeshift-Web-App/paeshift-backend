import googlemaps
from django.conf import settings
from django.contrib.gis.geos import Point
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from ninja import Router
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.timezone import now
from math import radians, sin, cos, sqrt, atan2
from decimal import Decimal
import requests
from django.db import transaction
from django.http import JsonResponse

# Import Models
from .schemas import *
from models import *

from jobs.models import *
from jobchat.models import *  # Add this import
from django.contrib.auth import get_user_model

# Initialize Router
router = Router(tags=["Jobchat"])
User = get_user_model()

# ✅ Weights for Scoring Applicants
WEIGHT_RATING = 0.4
WEIGHT_DISTANCE = 0.3
WEIGHT_EXPERIENCE = 0.2
WEIGHT_COMPLETION_RATE = 0.1



def geocode_address(address):
    """Convert address to latitude and longitude."""
    try:
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        geocode_result = gmaps.geocode(address)

        if geocode_result:
            loc = geocode_result[0]["geometry"]["location"]
            return Point(loc["lng"], loc["lat"], srid=4326)

    except Exception as e:
        print(f"Google Maps API Error: {e}")

    return None







@router.post("/update-location")
def update_location(request, lat: float, lng: float):
    """Update the user's location."""
    user = request.user
    location = Point(lng, lat, srid=4326)

    UserLocation.objects.update_or_create(
        user=user,
        defaults={"last_location": location, "is_online": True}
    )

    return {"status": "location_updated"}

@router.get("/track-applicant/{applicant_id}")
def track_applicant(request, applicant_id: int):
    """Retrieve the last known location of an applicant."""
    applicant = get_object_or_404(User, id=applicant_id)
    location_record = LocationHistory.objects.filter(user=applicant).last()

    if not location_record:
        return {"error": "No location data available"}

    return {
        "coordinates": {"lat": location_record.latitude, "lng": location_record.longitude},
        "last_updated": location_record.timestamp
    }

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_nearby_jobs(request):
    """Fetches jobs near the authenticated user's last known location."""
    user = request.user
    user_location = LocationHistory.objects.filter(user=user).last()

    if not user_location:
        return Response({"error": "Location not found"}, status=404)

    jobs = Job.objects.filter(status="upcoming")
    job_list = []

    for job in jobs:
        distance = calculate_distance(user_location.latitude, user_location.longitude, job.latitude, job.longitude)
        if distance <= 50:
            job_list.append({
                "id": job.id,
                "title": job.title,
                "shift_type": job.shift_type,
                "rate": job.rate,
                "distance": round(distance, 2)
            })

    return Response({"jobs": sorted(job_list, key=lambda x: x["distance"])}, status=200)

@router.post("/jobs/{job_id}/update-location")
def update_job_location(request, job_id: int, lat: float, lng: float):
    """Update the location of a job seeker for a specific job."""
    user = request.user
    location = Point(lng, lat, srid=4326)

    UserLocation.objects.update_or_create(
        user=user,
        defaults={"last_location": location, "is_online": True}
    )

    return {"message": f"Location updated for job {job_id}"}

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two latitude/longitude points using Haversine formula."""
    R = 6371.0  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Distance in km

@router.get("/jobs/{job_id}/best-applicants/")
def get_best_applicants(request, job_id: int):
    """Fetch and notify the best applicants for a job."""
    try:
        job = Job.objects.get(id=job_id)
        job_location = Point(job.longitude, job.latitude)

        candidates = Profile.objects.filter(
            industry=job.industry,
            subcategory=job.subcategory,
            is_active=True
        ).annotate(
            avg_rating=Avg("user__ratings_received__rating"),
            distance=Distance("last_location", job_location)
        ).order_by("-avg_rating", "distance")[:5]

        top_applicants = [
            {
                "id": candidate.user.id,
                "name": candidate.user.username,
                "rating": candidate.avg_rating or 0,
                "distance_km": round(candidate.distance.km, 2)
            }
            for candidate in candidates
        ]

        # 🔥 Notify matched users via WebSocket
        from channels.layers import get_channel_layer
        import asyncio

        channel_layer = get_channel_layer()
        for applicant in candidates:
            asyncio.run(channel_layer.group_send(
                f"user_matching_{applicant.user.id}",
                {
                    "type": "job_match_found",
                    "message": f"New job match found: {job.title}!",
                    "job_id": job.id
                }
            ))

        return {"top_applicants": top_applicants}

    except Job.DoesNotExist:
        return {"error": "Job not found"}, 404

