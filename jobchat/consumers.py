# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, LocationHistory
from jobs.models import Job
from django.contrib.auth import get_user_model
import requests
from django.conf import settings

User = get_user_model()

import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info(f"WebSocket connected: {self.channel_name}")
        self.job_id = self.scope['url_route']['kwargs']['job_id']
        self.room_group_name = f"chat_{self.job_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected: {self.channel_name}")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        logger.info(f"Received message: {text_data}")
        data = json.loads(text_data)
        message = data.get('message', '').strip()
        sender = self.scope["user"]

        if sender.is_authenticated and message:
            await self.save_message(sender, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": sender.username,
                }
            )

    async def chat_message(self, event):
        logger.info(f"Sending message: {event}")
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, sender, message):
        job = Job.objects.get(id=self.job_id)
        logger.info(f"Saving message: {message} by {sender.username}")
        return Message.objects.create(job=job, sender=sender, content=message)



class JobLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info(f"WebSocket connected: {self.channel_name}")
        self.job_id = self.scope["url_route"]["kwargs"]["job_id"]
        self.group_name = f"job_{self.job_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected: {self.channel_name}")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        logger.info(f"Received location data: {text_data}")
        data = json.loads(text_data)
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        user = self.scope["user"]

        if user.is_authenticated and latitude and longitude:
            address = await self.decode_address(latitude, longitude)
            await self.save_location(user, latitude, longitude, address)
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
        logger.info(f"Sending location update: {event}")
        await self.send(text_data=json.dumps(event))

    async def decode_address(self, lat, lon):
        return await database_sync_to_async(self._fetch_address_from_google)(lat, lon)

    def _fetch_address_from_google(self, lat, lon):
        api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
        if not api_key:
            return "API Key Missing"
        url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={api_key}"
        response = requests.get(url)
        data = response.json()

        if data.get("status") == "OK" and data.get("results"):
            return data["results"][0].get("formatted_address", "Unknown Location")
        return "Unknown Location"

    @database_sync_to_async
    def save_location(self, user, lat, lon, address):
        job = Job.objects.get(id=self.job_id)
        logger.info(f"Saving location: {lat}, {lon} by {user.username}")
        return LocationHistory.objects.create(job=job, user=user, latitude=lat, longitude=lon, address=address)