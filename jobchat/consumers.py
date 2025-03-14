import json
import requests
import logging
import asyncio
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
import django

django.setup()

from django.apps import apps

Message = apps.get_model("jobchat", "Message")
LocationHistory = apps.get_model("jobchat", "LocationHistory")
Job = apps.get_model("jobs", "Job")

User = get_user_model()
logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    """Handles real-time job chat messaging"""

    async def connect(self):
        self.job_id = self.scope['url_route']['kwargs']['job_id']
        self.room_group_name = f"chat_{self.job_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        logger.info(f"Chat WebSocket connected: {self.channel_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        logger.info(f"Chat WebSocket disconnected: {self.channel_name}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '').strip()
        sender = self.scope.get("user")

        if sender and sender.is_authenticated and message:
            await self.save_message(sender, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat_message", "message": message, "sender": sender.username}
            )

    async def chat_message(self, event):
        sender = event.get("sender", "Anonymous")
        message = event.get("message", "[No message]")
        await self.send(text_data=json.dumps({"sender": sender, "message": message}))

    @database_sync_to_async
    def save_message(self, sender, message):
        job = Job.objects.get(id=self.job_id)
        return Message.objects.create(job=job, sender=sender, content=message)


class JobLocationConsumer(AsyncWebsocketConsumer):
    """Handles real-time job location tracking"""

    async def connect(self):
        self.job_id = self.scope["url_route"]["kwargs"]["job_id"]
        self.group_name = f"job_{self.job_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        self.last_lat = None
        self.last_lon = None
        logger.info(f"Location WebSocket connected: {self.channel_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        logger.info(f"Location WebSocket disconnected: {self.channel_name}")

    async def receive(self, text_data):
        """Process received location data"""
        data = json.loads(text_data)

        if data.get("type") == "heartbeat":
            await self.send(text_data=json.dumps({"type": "heartbeat_ack"}))
            return

        user = self.scope.get("user")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if user and user.is_authenticated and latitude and longitude:
            asyncio.create_task(self.process_location(user, latitude, longitude))

    async def process_location(self, user, latitude, longitude):
        """Save or update location based on movement"""
        current_time = datetime.utcnow()

        # Get the last saved location
        last_location = await self.get_last_location(user)

        if last_location and last_location.latitude == latitude and last_location.longitude == longitude:
            # If the location is the same as the last one, just update the timestamp
            await self.update_last_location_time(last_location, current_time)
        else:
            # Save the new location if different
            await self.save_location(user, latitude, longitude, current_time)

        address = await self.decode_address(latitude, longitude)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "location_update",
                "latitude": latitude,
                "longitude": longitude,
                "address": address,
                "user": user.username,
            }
        )

    async def location_update(self, event):
        await self.send(text_data=json.dumps(event))

    async def decode_address(self, lat, lon):
        return await database_sync_to_async(self._fetch_address_from_google)(lat, lon)

    def _fetch_address_from_google(self, lat, lon):
        api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
        if not api_key:
            return "API Key Missing"

        url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={api_key}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data["results"][0].get("formatted_address", "Unknown Location") if data.get("status") == "OK" else "Unknown Location"
        except requests.RequestException:
            return "Unknown Location"

    @database_sync_to_async
    def get_last_location(self, user):
        """Get the last recorded location of the user"""
        return LocationHistory.objects.filter(user=user).order_by("-timestamp").first()

    @database_sync_to_async
    def save_location(self, user, lat, lon, timestamp):
        """Save user location to the database"""
        job = Job.objects.get(id=self.job_id)
        return LocationHistory.objects.create(job=job, user=user, latitude=lat, longitude=lon, timestamp=timestamp)

    @database_sync_to_async
    def update_last_location_time(self, last_location, new_timestamp):
        """Update the timestamp of the last saved location"""
        last_location.timestamp = new_timestamp
        last_location.save()
        
        
        
        
        
        
        
        


class JobMatchingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("job_matching", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("job_matching", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        if action == 'subscribe_jobs':
            await self.handle_job_subscription(data)
        elif action == 'update_location':
            await self.handle_location_update(data)


    async def receive(self, text_data):
        data = json.loads(text_data)
        job_id = data.get('job_id')
        job = Job.objects.get(id=job_id)
        
        applicants = await find_best_applicants(job)
        await self.send(text_data=json.dumps({
            "type": "match_results",
            "applicants": serialize_applicants(applicants)
        }))

    async def job_notification(self, event):
        await self.send(text_data=json.dumps(event["content"]))






    async def handle_job_subscription(self, data):
        user = self.scope['user']
        jobs = await self.get_nearby_jobs(user)
        await self.send(text_data=json.dumps({
            'type': 'job_list',
            'jobs': jobs
        }))

    async def handle_location_update(self, data):
        user = self.scope['user']
        lat = data.get('lat')
        lng = data.get('lng')
        await self.update_user_location(user, lat, lng)

    @database_sync_to_async
    def get_nearby_jobs(self, user):
        from django.contrib.gis.db.models.functions import Distance
        user_location = UserLocation.objects.get(user=user)
        
        return list(Job.objects.filter(
            status='active',
            location__dwithin=(user_location.last_location, 50000)  # 50km
        ).annotate(
            distance=Distance('location', user_location.last_location)
        ).order_by('distance')[:10].values(
            'id', 'title', 'shift_type', 'rate', 'distance'
        ))

    @database_sync_to_async
    def update_user_location(self, user, lat, lng):
        UserLocation.objects.update_or_create(
            user=user,
            defaults={
                'last_location': Point(lng, lat),
                'is_online': True
            }
        ) 
        
        
       
        