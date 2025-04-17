from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Candidate, Recruiter, Job, Application, SavedJob
from django.contrib import messages
from django.shortcuts import render
from .models import Job

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Job

from django.shortcuts import render
from .models import Job, Recruiter

from django.db.models import Q
from datetime import datetime

def home(request):
    jobs = Job.objects.all().order_by('-created_at')
    recruiters = Recruiter.objects.all()
    return render(request, 'home.html', {'jobs': jobs, 'recruiters': recruiters})


def aboutus(request):
    return render(request,"AboutUs.html")

def Careers(request):
    return render(request,"Careers.html")

def privacypoliccy(request):
    return render(request,"PrivacyPolicy.html")

def ts(request):
    return render(request,"TOS.html")



def career_tips(request):
    return render(request, 'careerstips.html')  # 'career_tips.html' is the name of your template

def user_logout(request):
    """
    Logs the user out and redirects to home.
    """
    logout(request)
    return redirect('home')

# Candidate Registration
def candidate_register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        username = email.split('@')[0]
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            role='candidate'
        )
        Candidate.objects.create(user=user)
        login(request, user)
        return redirect('candidate_dashboard')
    
    return render(request, 'auth/candidate_register.html')

# Recruiter Registration
def recruiter_register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        company_name = request.POST['company_name']
        username = email.split('@')[0]

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='recruiter'
        )
        Recruiter.objects.create(user=user, company_name=company_name)
        login(request, user)
        return redirect('recruiter_dashboard')
    
    return render(request, 'auth/recruiter_register.html')

# def user_login(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)
#             if user.role == 'candidate':
#                 return redirect('candidate_dashboard')
#             elif user.role == 'recruiter':
#                 return redirect('recruiter_dashboard')
#             else:
#                 return redirect('home')
#         else:
#             messages.error(request, "Invalid email or password.")
#             return redirect('login')
#     return render(request, 'login.html')



# Constants for user roles
CANDIDATE_ROLE = 'candidate'
RECRUITER_ROLE = 'recruiter'

def user_login(request):
    if request.method == "POST":
        # Retrieve email and password from POST data
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Log the user in
            login(request, user)

            # Determine target dashboard based on user role
            if user.role == CANDIDATE_ROLE:
                messages.success(request, f"Welcome to the Candidate Dashboard, {user.first_name}!")
                return redirect('candidate_dashboard')
            elif user.role == RECRUITER_ROLE:
                messages.success(request, f"Welcome to the Recruiter Dashboard, {user.first_name}!")
                return redirect('recruiter_dashboard')
            else:
                # Redirect to home for unhandled roles
                messages.warning(request, "Role not recognized. Redirecting to home.")
                return redirect('home')
        else:
            # Authentication failed
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    # Render the login page for GET requests
    return render(request, 'login.html')


from django.shortcuts import render, redirect
from core.models import User
from django.contrib import messages

def forgot_password(request):
    if request.method == "POST":
        # Retrieve the username and email from the POST data
        username = request.POST.get("username")
        email = request.POST.get("email")

        # Try to get the user based on the username and email
        try:
            user = User.objects.get(username=username, email=email)

            # If user is found, redirect to reset password page
            messages.success(request, "We found your account! Please create a new password.")
            return redirect('reset_password', user_id=user.id)
        except User.DoesNotExist:
            # If no user is found with that combination
            messages.error(request, "No user found with this username and email combination.")
            return redirect('forgot_password')

    # Render forgot password form
    return render(request, 'auth/forgot_password.html')


def reset_password(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('forgot_password')

    if request.method == "POST":
        # Get the new password from the POST data
        new_password = request.POST.get("new_password")
        if new_password:
            # Set the new password and save the user
            user.set_password(new_password)
            user.save()
            messages.success(request, "Your password has been reset successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please enter a valid password.")

    # Render reset password form
    return render(request, 'auth/reset_password.html', {'user_id': user.id})


# Candidate Dashboard
@login_required
def candidate_dashboard(request):
    candidate = get_object_or_404(Candidate, user=request.user)

    jobs = Job.objects.all().select_related('posted_by').order_by('-created_at')

    # Get filter values, strip spaces
    title = request.GET.get('title', '').strip()
    location = request.GET.get('location', '').strip()
    salary = request.GET.get('salary', '').strip()
    posted_at = request.GET.get('posted_at', '').strip()
    job_type = request.GET.get('job_type', '').strip()  # Added job_type filter

    # Apply filters only if values are present
    if title:
        jobs = jobs.filter(title__icontains=title)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if salary:
        try:
            jobs = jobs.filter(salary__gte=int(salary))
        except ValueError:
            pass
    if posted_at:
        try:
            date = datetime.strptime(posted_at, "%Y-%m-%d").date()
            jobs = jobs.filter(created_at__date=date)
        except ValueError:
            pass
    if job_type:  # Apply job_type filter
        jobs = jobs.filter(job_type=job_type)

    return render(request, 'candidate/dashboard.html', {
        'candidate': candidate,
        'jobs': jobs,
        'filters': {
            'title': title,
            'location': location,
            'salary': salary,
            'posted_at': posted_at,
            'job_type': job_type  # Add job_type to filters dictionary
        }
    })



# Recruiter Dashboard
@login_required
def recruiter_dashboard(request):
    recruiter = get_object_or_404(Recruiter, user=request.user)
    jobs = Job.objects.filter(posted_by=recruiter)
    return render(request, 'recruiter/dashboard.html', {'recruiter': recruiter, 'jobs': jobs})

# Create Job (Recruiter Only)
@login_required
def create_job(request):
    if request.user.role != 'recruiter':
        return redirect('home')
    recruiter = get_object_or_404(Recruiter, user=request.user)
    if request.method == "POST":
        Job.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            requirements=request.POST.get('requirements', ''),
            location=request.POST['location'],
            salary=request.POST.get('salary', None),
            posted_by=recruiter,
            job_type=request.POST['job_type']  # Add this field
        )
        return redirect('recruiter_dashboard')
    return render(request, 'recruiter/create_job.html')


@login_required
def update_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Make sure the user is the recruiter who posted the job
    if request.user.role != 'recruiter' or job.posted_by.user != request.user:
        return redirect('home')

    if request.method == "POST":
        job.title = request.POST['title']
        job.description = request.POST['description']
        job.requirements = request.POST.get('requirements', '')
        job.location = request.POST['location']
        job.salary = request.POST.get('salary', None)
        job.job_type = request.POST['job_type']
        job.save()
        return redirect('recruiter_dashboard')

    context = {
        'job': job
    }
    return render(request, 'recruiter/update_job.html', context)

# Delete Job (Recruiter Only)
@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by__user=request.user)
    job.delete()
    return redirect('recruiter_dashboard')


from django.shortcuts import render, get_object_or_404
from .models import Job, SavedJob, Application, Candidate

def job_details(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    saved = False
    applied = False

    # Check if user is a candidate
    if request.user.is_authenticated and hasattr(request.user, 'candidate'):
        candidate = Candidate.objects.get(user=request.user)

        # Check if job is saved
        saved = SavedJob.objects.filter(candidate=candidate, job=job).exists()

        # Check if job is applied
        applied = Application.objects.filter(candidate=candidate, job=job).exists()

    return render(
        request,
        "job/details.html",
        {
            "job": job,
            "saved": saved,
            "applied": applied,
        }
    )


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, Application, Candidate

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    candidate = get_object_or_404(Candidate, user=request.user)

    # Check if the candidate already applied
    if Application.objects.filter(job=job, candidate=candidate).exists():
        return redirect('job_details', job_id=job_id)

    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter', '')
        Application.objects.create(job=job, candidate=candidate, cover_letter=cover_letter)
        return redirect('candidate_dashboard')

    return render(request, 'job/apply.html', {'job': job})




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Candidate

@login_required
def candidate_profile(request):
    candidate = get_object_or_404(Candidate, user=request.user)

    if request.method == 'POST':
        candidate.user.first_name = request.POST.get('first_name', candidate.user.first_name)
        candidate.user.last_name = request.POST.get('last_name', candidate.user.last_name)
        candidate.user.middle_name = request.POST.get('middle_name', candidate.user.middle_name)
        candidate.education_details = request.POST.get('education_details', candidate.education_details)
        candidate.certifications = request.POST.get('certifications', candidate.certifications)
        candidate.address = request.POST.get('address', candidate.address)
        candidate.current_status = request.POST.get('current_status', candidate.current_status)

        if 'profile_photo' in request.FILES:
            candidate.profile_photo = request.FILES['profile_photo']
        if 'resume' in request.FILES:
            candidate.resume = request.FILES['resume']

        candidate.user.save()
        candidate.save()
        return redirect('candidate_dashboard')

    return render(request, 'candidate/profile.html', {'candidate': candidate})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Candidate

@login_required
def update_candidate_profile(request):
    candidate = get_object_or_404(Candidate, user=request.user)

    if request.method == 'POST':
        # Update user info
        candidate.user.first_name = request.POST.get('first_name', candidate.user.first_name)
        candidate.user.middle_name = request.POST.get('middle_name', candidate.user.middle_name)
        candidate.user.last_name = request.POST.get('last_name', candidate.user.last_name)
        candidate.user.date_of_birth = request.POST.get('date_of_birth', candidate.user.date_of_birth)
        
        # Update candidate-specific fields
        candidate.education_details = request.POST.get('education_details', candidate.education_details)
        candidate.certifications = request.POST.get('certifications', candidate.certifications)
        candidate.address = request.POST.get('address', candidate.address)
        candidate.current_status = request.POST.get('current_status', candidate.current_status)

        # Handle file uploads
        if 'profile_photo' in request.FILES:
            candidate.profile_photo = request.FILES['profile_photo']
        if 'resume' in request.FILES:
            candidate.resume = request.FILES['resume']

        # Save changes
        candidate.user.save()
        candidate.save()
        messages.success(request, "Your profile has been updated successfully!")
        return redirect('candidate_dashboard')

    return render(request, 'candidate/update_profile.html', {'candidate': candidate})



@login_required
def save_job(request, job_id):
    # Only allow candidates to save a job
    if request.user.role != 'candidate':
        return redirect('job_details', job_id=job_id)
    candidate = get_object_or_404(Candidate, user=request.user)
    job = get_object_or_404(Job, id=job_id)
    # Create a SavedJob entry if not already saved
    if not SavedJob.objects.filter(candidate=candidate, job=job).exists():
        SavedJob.objects.create(candidate=candidate, job=job)
    return redirect('job_details', job_id=job_id)

@login_required
def unsave_job(request, job_id):
    # Only allow candidates to unsave a job
    if request.user.role != 'candidate':
        return redirect('job_details', job_id=job_id)
    candidate = get_object_or_404(Candidate, user=request.user)
    job = get_object_or_404(Job, id=job_id)
    saved_job = SavedJob.objects.filter(candidate=candidate, job=job)
    if saved_job.exists():
        saved_job.delete()
    return redirect('job_details', job_id=job_id)




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Recruiter, Job, Application

@login_required
def job_applicants(request, job_id):
    # Ensure only recruiters can access this view
    if request.user.role != 'recruiter':
        return redirect('home')
        
    recruiter = get_object_or_404(Recruiter, user=request.user)
    # Get the job ensuring it belongs to this recruiter
    job = get_object_or_404(Job, id=job_id, posted_by=recruiter)
    # Fetch all applications for this job
    applications = Application.objects.filter(job=job)
    return render(request, 'recruiter/job_applicants.html', {
        'job': job,
        'applications': applications
    })

@login_required
def view_candidate_profile(request, candidate_id):
    # Ensure only recruiters can access this view
    if request.user.role != 'recruiter':
        return redirect('home')
    
    candidate = get_object_or_404(Candidate, id=candidate_id)
    return render(request, 'recruiter/candidate_profile.html', {'candidate': candidate})

@login_required
def update_recruiter_profile(request):
    recruiter = get_object_or_404(Recruiter, user=request.user)
    
    if request.method == "POST":
        recruiter.company_name = request.POST.get("company_name", recruiter.company_name)
        recruiter.established_year = request.POST.get("established_year", recruiter.established_year)
        recruiter.company_address = request.POST.get("company_address", recruiter.company_address)
        recruiter.hr_name = request.POST.get("hr_name", recruiter.hr_name)
        recruiter.company_description = request.POST.get("company_description", recruiter.company_description)
        
        if "company_logo" in request.FILES:
            recruiter.company_logo = request.FILES["company_logo"]
        
        recruiter.save()
        messages.success(request, "Your profile has been updated successfully!")
        return redirect("recruiter_dashboard")
    
    return render(request, "recruiter/update_profile.html", {"recruiter": recruiter})


def company_profile(request, recruiter_id):
    recruiter = get_object_or_404(Recruiter, id=recruiter_id)
    return render(request, 'recruiter/profile.html', {'recruiter': recruiter})






def dashboard_redirect(request):
    if request.user.is_authenticated:
        if request.user.role == 'candidate':
            return redirect('candidate_dashboard')  # Define the candidate dashboard URL in your urls.py
        elif request.user.role == 'recruiter':
            return redirect('recruiter_dashboard')  # Define the recruiter dashboard URL in your urls.py
        else:
            return redirect('home')  # Redirect elsewhere if the role doesn't match
    return redirect('login')  # Redirect to login if user is not authenticated
