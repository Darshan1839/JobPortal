from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=[('candidate', 'Candidate'), ('recruiter', 'Recruiter')])
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

# Candidate Model
class Candidate(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    education_details = models.TextField(blank=True)
    certifications = models.TextField(blank=True, default="")  # ✅ Allow empty & set default

    address = models.CharField(max_length=255, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    current_status = models.CharField(max_length=100, blank=True)

# Recruiter Model

class Recruiter(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, default='Unknown Company')
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    established_year = models.PositiveIntegerField(blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)
    hr_name = models.CharField(max_length=100, blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)  # New field for company description

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.company_name})"


# Job Model
class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('fresher', 'Fresher'),
        ('experienced', 'Experienced'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField(blank=True, default="")
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=15, choices=JOB_TYPE_CHOICES, default='fresher')  # 👈 New Field
    posted_by = models.ForeignKey('Recruiter', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Application Model
class Application(models.Model):
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    cover_letter = models.TextField(blank=True, default="")
    applied_at = models.DateTimeField(auto_now_add=True)

# Saved Jobs Model
class SavedJob(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.user.first_name} saved {self.job.title}"
