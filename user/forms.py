from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [("job_seeker", "Job Seeker"), ("employer", "Employer")]
    STATUS_CHOICES = [("fresher", "Fresher"), ("experienced", "Experienced")]

    role = forms.ChoiceField(choices=ROLE_CHOICES)
    phone = forms.CharField(max_length=15)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    current_status = forms.ChoiceField(choices=STATUS_CHOICES)
    experience_years = forms.IntegerField(required=False, min_value=0)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]
        widgets = {"password": forms.PasswordInput()}

    def clean(self):
        cleaned_data = super().clean()
        current_status = cleaned_data.get("current_status")
        experience_years = cleaned_data.get("experience_years")

        if current_status == "experienced" and not experience_years:
            raise forms.ValidationError("Please enter your years of experience.")

        return cleaned_data
