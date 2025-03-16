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

# Import Models
from jobs.models import Job, Application
from jobchat.models import LocationHistory
from users.models import Profile, UserLocation
from django.contrib.auth import get_user_model

# Initialize Router
router = Router(tags=["Jobchat"])
User = get_user_model()

# ✅ Weights for Scoring Applicants
WEIGHT_RATING = 0.4
WEIGHT_DISTANCE = 0.3
WEIGHT_EXPERIENCE = 0.2
WEIGHT_COMPLETION_RATE = 0.1


# -------------------------------------------------------------------
# 📌 FIND BEST APPLICANTS
# -------------------------------------------------------------------
def find_best_applicants(job, max_distance_km=50):
    """Find the best applicants for a given job."""
    
    job_lat, job_lon = job.latitude, job.longitude
    if not job_lat or not job_lon:
        return []

    candidates = (
        Profile.objects.filter(industry=job.industry, subcategory=job.subcategory, is_active=True)
        .annotate(
            avg_rating=Avg("user__ratings_received__rating"),
            total_jobs_completed=Count("user__accepted_jobs"),
            total_applications=Count("user__applications"),
            distance=Count("user__location")
        )
        .select_related("user")
    )

    ranked_candidates = []
    for candidate in candidates:
        user_loc = candidate.user.location
        if user_loc and user_loc.latitude and user_loc.longitude:
            distance = calculate_distance(job_lat, job_lon, user_loc.latitude, user_loc.longitude)
            if distance <= max_distance_km:
                score = (
                    (candidate.avg_rating or 0) * WEIGHT_RATING +
                    max(0, (50 - distance) / 50) * WEIGHT_DISTANCE +
                    (candidate.total_jobs_completed or 0) / 10 * WEIGHT_EXPERIENCE +
                    ((candidate.total_jobs_completed / candidate.total_applications) if candidate.total_applications else 0) * WEIGHT_COMPLETION_RATE
                )
                ranked_candidates.append((candidate, score))

    return [candidate[0] for candidate in sorted(ranked_candidates, key=lambda x: x[1], reverse=True)[:10]]


# -------------------------------------------------------------------
# 📌 GEOCODE ADDRESS (Using Google Maps API)
# -------------------------------------------------------------------
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


# -------------------------------------------------------------------
# 📌 UPDATE USER LOCATION
# -------------------------------------------------------------------
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


# -------------------------------------------------------------------
# 📌 TRACK APPLICANT LOCATION
# -------------------------------------------------------------------
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


# -------------------------------------------------------------------
# 📌 FETCH NEARBY JOBS
# -------------------------------------------------------------------
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


# -------------------------------------------------------------------
# 📌 UPDATE JOB LOCATION
# -------------------------------------------------------------------
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


# -------------------------------------------------------------------
# 📌 CALCULATE DISTANCE (Haversine Formula)
# -------------------------------------------------------------------
def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two latitude/longitude points using Haversine formula."""
    R = 6371.0  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Distance in km



@router.post("/update-location")
def update_location(request, lat: float, lng: float):
    user = request.user
    location = Point(lng, lat, srid=4326)
    UserLocation.objects.update_or_create(
        user=user,
        defaults={'last_location': location, 'is_online': True}
    )
    return {"status": "location_updated"}

@router.get("/track-applicant/{applicant_id}")
def track_applicant(request, applicant_id: int):
    applicant = User.objects.get(id=applicant_id)
    return {
        "location": json.loads(applicant.userlocation.last_location.geojson),
        "last_updated": applicant.userlocation.last_online
    }