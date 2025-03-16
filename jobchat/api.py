import googlemaps
from django.conf import settings
from django.contrib.gis.geos import Point, GEOSGeometry
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from ninja import Router
from jobs.models import Job
from users.models import Profile, UserLocation
from django.contrib.auth import get_user_model

# ==============================
# 📌 Initialize Router & User Model
# ==============================
router = Router(tags=["Jobchat"])
User = get_user_model()

# Weights for scoring applicants
WEIGHT_RATING = 0.4
WEIGHT_DISTANCE = 0.3
WEIGHT_EXPERIENCE = 0.2
WEIGHT_COMPLETION_RATE = 0.1


def find_best_applicants(job):
    """Find and rank the best applicants for a given job based on multiple factors."""

    candidates = Profile.objects.filter(
        industry=job.industry,
        subcategory=job.subcategory,
        is_active=True
    ).annotate(
        avg_rating=Avg("user__ratings_received__rating"),
        total_jobs_completed=Count("user__accepted_jobs"),
        total_applications=Count("user__applications"),
        distance=Distance("last_location", Point(job.longitude, job.latitude))
    ).select_related("user")  # Optimize query

    ranked_candidates = [
        (
            candidate,
            (
                (candidate.avg_rating or 0) * WEIGHT_RATING +
                max(0, (50 - candidate.distance.km) / 50) * WEIGHT_DISTANCE +
                (candidate.total_jobs_completed or 0) / 10 * WEIGHT_EXPERIENCE +
                ((candidate.total_jobs_completed / candidate.total_applications) if candidate.total_applications else 0) * WEIGHT_COMPLETION_RATE
            )
        )
        for candidate in candidates
    ]

    # Sort candidates by total score (highest first) and return top 10
    return [candidate[0] for candidate in sorted(ranked_candidates, key=lambda x: x[1], reverse=True)[:10]]


def geocode_address(address):
    """Convert address to latitude and longitude using Google Maps API."""
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
    """Update user location and mark them as online."""
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
    location_record = applicant.location.last()

    if not location_record:
        return {"error": "No location data available"}

    location = GEOSGeometry(location_record.last_location.geojson)
    
    return {
        "coordinates": {"lat": location.y, "lng": location.x},
        "last_updated": location_record.last_online
    }


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
