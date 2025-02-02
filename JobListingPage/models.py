from django.db import models
from authUser.models import CustomUser
from authUser.models import Profile

# User Profile Model
# class UserProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
#     rating = models.FloatField(default=0.0)

#     def __str__(self):
#         return self.user.username

# Job Listing Model
class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    contract_duration = models.CharField(max_length=50)  # e.g., "2hrs Contract"
    date_posted = models.DateTimeField(auto_now_add=True)
    job_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    applicants_needed = models.PositiveIntegerField(default=1)
    posted_by = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Job Application Model
class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ], default='Pending')

    def __str__(self):
        return f"{self.applicant.user.username} - {self.job.title}"

# Saved Jobs Model
class SavedJob(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.username} saved {self.job.title}"
