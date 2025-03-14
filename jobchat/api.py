
import googlemaps

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