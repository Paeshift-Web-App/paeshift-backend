from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Job, SavedJob

class SaveJobTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.job = Job.objects.create(title='Test Job', client=self.user)
        self.url = reverse('save_job', kwargs={'job_id': self.job.id})
