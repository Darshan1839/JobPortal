from django import forms
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('Candidate', 'Candidate'),
    ('Recruiter', 'Recruiter'),
]

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="User Role")
    phone = forms.CharField(max_length=15, required=True, label="Phone Number")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'phone']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned_data
