# jobs/utils/matching.py
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Q, F

def find_best_applicants(job, max_distance_km=50):
    return User.objects.annotate(
        distance=Distance('userlocation__last_location', job.location)
    ).filter(
        Q(profile__available_shifts__contains=job.shift_type) &
        Q(profile__rating__gte=4.0) &
        Q(userlocation__is_online=True) &
        Q(userlocation__distance__lte=50000)  # 50km in meters
    ).order_by(
        '-profile__premium_tier',
        '-profile__rating',
        'distance'
    )[:10]  # Top 10 candidates