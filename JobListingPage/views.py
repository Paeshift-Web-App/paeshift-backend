from django.shortcuts import render
from rest_framework import viewsets
from.models import Profile, Job, JobApplication, SavedJob
from.serializers import UserProfileSerializer, JobSerializer, JobApplicationSerializer, SavedJobSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

class SavedJobViewSet(viewsets.ModelViewSet):
    queryset = SavedJob.objects.all()
    serializer_class = SavedJobSerializer
