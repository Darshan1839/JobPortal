from django.contrib import admin
from .models import User, Candidate, Recruiter, Job, Application, SavedJob

# User Admin Panel
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

# Candidate Admin Panel
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_date_of_birth', 'education_details', 'address')
    search_fields = ('user__first_name', 'user__last_name', 'education_details')

    # Display date_of_birth from User model
    def get_date_of_birth(self, obj):
        return obj.user.date_of_birth
    get_date_of_birth.short_description = 'Date of Birth'

# Recruiter Admin Panel
@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name')
    search_fields = ('user__first_name', 'user__last_name', 'company_name')

# Job Admin Panel
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'salary', 'posted_by', 'created_at')
    search_fields = ('title', 'location', 'posted_by__user__first_name')

# Application Admin Panel
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'get_status', 'applied_at')
    list_filter = ('status', 'job__title', 'candidate__user__first_name')
    search_fields = ('candidate__user__first_name', 'candidate__user__last_name', 'job__title')

    # Ensure status is displayed correctly
    def get_status(self, obj):
        return obj.status
    get_status.short_description = 'Status'

# Saved Job Admin Panel
@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'saved_at')
    search_fields = ('candidate__user__first_name', 'job__title')
