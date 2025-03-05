
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ("job_seeker", "Job Seeker"),
        ("employer", "Employer"),
    ]
    
    STATUS_CHOICES = [
        ("fresher", "Fresher"),
        ("experienced", "Experienced"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="job_seeker")
    phone = models.CharField(max_length=15, blank=True, null=True)
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="fresher")
    experience_years = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username
