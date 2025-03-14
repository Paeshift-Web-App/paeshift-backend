# tracking/api.py
from ninja import Router
from django.contrib.gis.geos import Point

router = Router(tags=["Tracking"])

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