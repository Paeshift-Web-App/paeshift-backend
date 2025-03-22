import json
import logging
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from jobchat.models import LocationHistory, Message
from jobs.models import Job

logger = logging.getLogger(__name__)

User = get_user_model()


# =========================================================
# ✅ CHAT CONSUMER: Handles Job Chat Messaging
# =========================================================
class ChatConsumer(AsyncWebsocketConsumer):
    """Handles real-time job chat messaging"""

    async def connect(self):
        self.job_id = self.scope["url_route"]["kwargs"]["job_id"]
        self.room_group_name = f"chat_{self.job_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        logger.info(f"✅ Chat WebSocket connected for Job #{self.job_id}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        logger.info(f"❌ Chat WebSocket disconnected for Job #{self.job_id}")

    async def receive(self, text_data):
        """Handles incoming chat messages"""
        data = json.loads(text_data)
        message = data.get("message", "").strip()
        sender = self.scope["user"]

        if sender.is_authenticated and message:
            await self.save_message(sender, message)
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "message": message, "sender": sender.username}
            )

    async def chat_message(self, event):
        """Sends chat messages to all connected users"""
        await self.send(text_data=json.dumps({"sender": event.get("sender", "Anonymous"), "message": event.get("message", "[No message]")}))

    @database_sync_to_async
    def save_message(self, sender, message):
        """Saves the message in the database"""
        return Message.objects.create(job_id=self.job_id, sender=sender, content=message)


# =========================================================
# ✅ JOB LOCATION CONSUMER: Handles Real-time Job Location Tracking
# =========================================================
class JobLocationConsumer(AsyncWebsocketConsumer):
    """Handles real-time job location tracking"""

    async def connect(self):
        self.job_id = self.scope["url_route"]["kwargs"]["job_id"]
        self.group_name = f"job_{self.job_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        logger.info(f"✅ Location WebSocket connected: {self.channel_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        logger.info(f"❌ Location WebSocket disconnected: {self.channel_name}")

    async def receive(self, text_data):
        """Processes received location data"""
        data = json.loads(text_data)

        if data.get("type") == "heartbeat":
            await self.send(text_data=json.dumps({"type": "heartbeat_ack"}))
            return

        user = self.scope.get("user")
        if user.is_authenticated and data.get("latitude") and data.get("longitude"):
            await self.process_location(user, data["latitude"], data["longitude"])

    async def process_location(self, user, latitude, longitude):
        """Saves or updates the user's location"""
        timestamp = datetime.utcnow()
        last_location = await self.get_last_location(user)

        if last_location and last_location.latitude == latitude and last_location.longitude == longitude:
            await self.update_last_location_time(last_location, timestamp)
        else:
            await self.save_location(user, latitude, longitude, timestamp)

        await self.channel_layer.group_send(
            self.group_name, {"type": "location_update", "latitude": latitude, "longitude": longitude, "user": user.username}
        )

    async def location_update(self, event):
        """Sends updated location data to frontend"""
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_last_location(self, user):
        """Gets the last recorded location of the user"""
        return LocationHistory.objects.filter(user=user).order_by("-timestamp").first()

    @database_sync_to_async
    def save_location(self, user, lat, lon, timestamp):
        """Saves user location to the database"""
        return LocationHistory.objects.create(job_id=self.job_id, user=user, latitude=lat, longitude=lon, timestamp=timestamp)

    @database_sync_to_async
    def update_last_location_time(self, last_location, timestamp):
        """Updates the timestamp of the last saved location"""
        last_location.timestamp = timestamp
        last_location.save()


# =========================================================
# ✅ JOB MATCHING CONSUMER: Handles Real-time Job Matching
# =========================================================
class JobMatchingConsumer(AsyncWebsocketConsumer):
    """Handles real-time job matching and updates."""

    async def connect(self):
        """Handles WebSocket connection."""
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.room_group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            logger.info(f"✅ {self.user.username} connected to Job Matching WebSocket.")
        else:
            await self.close()

    async def disconnect(self, close_code):
        """Handles WebSocket disconnection."""
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Handles incoming WebSocket messages."""
        data = json.loads(text_data)
        if data.get("action") == "subscribe_jobs":
            await self.send_nearby_jobs()

    async def send_nearby_jobs(self):
        """Sends nearby job listings to the user."""
        jobs = await self.get_nearby_jobs(self.user)
        await self.send(text_data=json.dumps({"type": "job_list", "jobs": jobs}))

    @database_sync_to_async
    def get_nearby_jobs(self, user):
        """Fetches jobs near the user's location."""
        user_location = LocationHistory.objects.filter(user=user).last()
        if not user_location:
            return []

        jobs = Job.objects.filter(status="upcoming")
        return [
            {
                "id": job.id,
                "title": job.title,
                "shift_type": job.shift_type,
                "rate": job.rate,
            }
            for job in jobs
        ]


# =========================================================
# ✅ JOB APPLICATION CONSUMER: Handles Job Application Notifications
# =========================================================
class JobApplicationConsumer(AsyncWebsocketConsumer):
    """Handles real-time job application notifications"""

    async def connect(self):
        self.job_id = self.scope["url_route"]["kwargs"]["job_id"]
        self.group_name = f"job_applications_{self.job_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)


# =========================================================
# ✅ PAYMENT NOTIFICATION CONSUMER: Handles Payment Notifications
# =========================================================
class PaymentNotificationConsumer(AsyncWebsocketConsumer):
    """Handles real-time payment success notifications"""

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.group_name = f"user_payments_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def payment_success(self, event):
        """Send payment success notification to user"""
        await self.send(text_data=json.dumps(event))
