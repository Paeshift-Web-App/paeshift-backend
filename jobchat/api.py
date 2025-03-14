
import googlemaps
def find_best_applicants(job):
    """Finds and ranks the best applicants for a given job based on multiple dynamic factors."""
    
    # Get all users that match the job industry and subcategory
    candidates = Profile.objects.filter(
        industry=job.industry,
        subcategory=job.subcategory,
        is_active=True  # Only active job seekers
    ).annotate(
        avg_rating=Avg("user__ratings_received__rating"),
        total_jobs_completed=Count("user__accepted_jobs"),
        total_applications=Count("user__applications"),
        distance=Distance('last_location', Point(job.longitude, job.latitude))
    )

    # Calculate weighted score for each candidate
    ranked_candidates = []
    for candidate in candidates:
        rating_score = (candidate.avg_rating or 0) * WEIGHT_RATING
        distance_score = max(0, (50 - candidate.distance.km) / 50) * WEIGHT_DISTANCE  # Normalize 50km radius
        experience_score = (candidate.total_jobs_completed or 0) / 10 * WEIGHT_EXPERIENCE  # Normalize out of 10 jobs
        completion_rate = (candidate.total_jobs_completed / candidate.total_applications) if candidate.total_applications else 0
        completion_score = completion_rate * WEIGHT_COMPLETION_RATE

        total_score = rating_score + distance_score + experience_score + completion_score
        ranked_candidates.append((candidate, total_score))

    # Sort candidates by total score (highest first)
    ranked_candidates.sort(key=lambda x: x[1], reverse=True)

    return [candidate[0] for candidate in ranked_candidates[:10]]  # Return top 10 matches

def geocode_address(address):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        loc = geocode_result[0]['geometry']['location']
        return Point(loc['lng'], loc['lat'])
    return None

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
    from django.contrib.gis.geos import GEOSGeometry
    applicant = User.objects.get(id=applicant_id)
    location = GEOSGeometry(applicant.location.last_location.geojson)
    
    return {
        "coordinates": {
            "lat": location.y,
            "lng": location.x
        },
        "last_updated": applicant.location.last_online
    }