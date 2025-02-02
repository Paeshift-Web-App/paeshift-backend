from rest_framework import serializers
from .models import Job, JobApplication, SavedJob
from authUser.models import Profile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'profile_picture', 'rating']

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'contract_duration', 'date_posted', 'job_date', 'location', 'payment', 'applicants_needed', 'posted_by']

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'applicant', 'status']

class SavedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJob
        fields = ['id', 'user', 'job', 'saved_on']