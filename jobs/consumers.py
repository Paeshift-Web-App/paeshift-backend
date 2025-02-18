# jobs/consumers.py

import json
import requests
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings
from django.utils import timezone

from .models import Job, LocationHistory

class JobLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Called when a WebSocket connection is established.
        We'll join a group named "job_<job_id>" so multiple participants
        of this job can share and receive location updates in real time.
        """
        self.job_id = self.scope["url_route"]["kwargs"]["job_id"]
        self.group_name = f"job_{self.job_id}"

        # Join the group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print(f"WebSocket connected for Job #{self.job_id}")

    async def disconnect(self, close_code):
        """
        Called when WebSocket disconnects.
        We'll remove the connection from the group.
        """
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"WebSocket disconnected from Job #{self.job_id}")

    async def receive(self, text_data):
        """
        Called when the frontend sends JSON data with "latitude" and "longitude".
        e.g. {"latitude": 6.5244, "longitude": 3.3792}
        """
        data = json.loads(text_data)
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        # 1) Reverse geocode to get an address (optional)
        address = await self.decode_address(latitude, longitude)

        # 2) Save location in DB (LocationHistory + update Job's last location)
        await self.save_location_to_db(latitude, longitude, address)

        # 3) Broadcast location to everyone in the job_<job_id> group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "location_update",
                "latitude": latitude,
                "longitude": longitude,
                "address": address,
            }
        )

    async def location_update(self, event):
        """
        Group broadcast handler: sends the updated location to all group members
        connected to this job.
        """
        await self.send(text_data=json.dumps({
            "latitude": event["latitude"],
            "longitude": event["longitude"],
            "address": event["address"],
        }))

    async def decode_address(self, lat, lon):
        """
        Async helper to call a synchronous function that fetches the address from Google Maps.
        """
        return await database_sync_to_async(self._fetch_address_from_google)(lat, lon)

    def _fetch_address_from_google(self, lat, lon):
        """
        Synchronous function that calls the Google Maps Geocoding API.
        If you have a real key, store it in settings.GOOGLE_MAPS_API_KEY.
        """
        api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', 'YOUR_API_KEY')
        url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={api_key}"
        response = requests.get(url)
        data = response.json()

        if data["status"] == "OK" and data["results"]:
            return data["results"][0]["formatted_address"]
        return "Unknown Location"

    async def save_location_to_db(self, lat, lon, address):
        """
        Async wrapper that calls a sync method to store the location in DB.
        """
        return await database_sync_to_async(self._save_location)(lat, lon, address)

    def _save_location(self, lat, lon, address):
        """
        1) Insert a record into LocationHistory for historical data.
        2) Update the Job's last shared location fields.
        """
        # Get the job
        job = Job.objects.get(id=self.job_id)

        # Identify the user from the scope if they're authenticated
        user = self.scope["user"] if self.scope["user"].is_authenticated else None

        # Create a LocationHistory record
        LocationHistory.objects.create(
            job=job,
            user=user,
            latitude=lat,
            longitude=lon,
            address=address,
            timestamp=timezone.now()
        )

        # Update the job's last location fields
        job.last_latitude = lat
        job.last_longitude = lon
        job.last_address = address
        job.last_location_update = timezone.now()
        job.save()

        return True
