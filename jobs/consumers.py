import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import database_sync_to_async
from .models import Application

class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract job_id from URL
        self.job_id = self.scope["url_route"]["kwargs"]["job_id"]

        # Check if the user is authenticated
        if self.scope["user"] is None or isinstance(self.scope["user"], AnonymousUser):
            await self.close()
            return

        # Check if user is accepted for this job
        is_allowed = await self.is_accepted_applicant(self.scope["user"].id, self.job_id)
        if not is_allowed:
            # Not an accepted applicant => deny
            await self.close()
            return

        # Otherwise, join the job-specific group
        self.group_name = f"job_{self.job_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """
        If the client or applicant sends data over the socket,
        you can handle it here. Typically, the client might not 
        need to receive data from an applicant.
        """
        data = json.loads(text_data)
        # Optionally handle messages from applicants

    async def location_update(self, event):
        """
        Called when the server sends group_send(..., type="location_update").
        We forward the updated location to all group members (accepted applicants).
        """
        await self.send(json.dumps({
            "latitude": event["latitude"],
            "longitude": event["longitude"],
        }))

    @database_sync_to_async
    def is_accepted_applicant(self, user_id, job_id):
        """
        Check if there's an Application for this user & job with is_accepted=True
        """
        return Application.objects.filter(
            applicant_id=user_id,
            job_id=job_id,
            is_accepted=True
        ).exists()
