from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username=models.CharField(null=True, blank=True, max_length=30)
    email= models.EmailField(unique=True)
    firstName=models.CharField(max_length=100, null=True, blank=True)
    lastName=models.CharField(max_length=100, null=True, blank=True)
    otp=models.CharField(max_length=100)
    refresh_token=models.CharField(unique=True, null=True, max_length=100)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
    # class Meta:
    #     verbose_name= ["CustomUser"]
    #     verbose_name_plural = ["CustomUsers"]
    
    def __str__(self) -> str:
        return f'{self.lastName} - {self.email}'
    
    def save(self, *args,**kwargs):
        emailUserName = self.email.split("@")
        if self.username == "" or self.username==None:
            self.username = emailUserName
            
        else: self.username 
            
        super(CustomUser, self).save(*args, **kwargs)
        
        
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="user_image", null=True, blank=True)
    firstName=models.CharField(max_length=100, null=True, blank=True)
    lastName=models.CharField(max_length=100, null=True, blank=True)
    location=models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=400, null=True, blank=True)
    rating= models.FloatField(default=0.0)
    date=models.DateTimeField(auto_now_add=True)
    
    
    # class Meta:
    #     verbose_name = ["Profile"]
    #     verbose_name_plural = ["Profiles"]
    
    def __str__(self):
        if self.lastName:
            return self.lastName
        else:
            return self.user.username
        
        
        
    def save(self, *args,**kwargs):
        
        if self.lastName == "" or self.lastName==None:
            self.lastName = self.user.username
            
        
            
        super(Profile, self).save(*args, **kwargs)
    
    