from django.shortcuts import render,redirect

# Create your views here.


from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import UserRegistrationForm


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .models import Profile

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Check if user already exists
            if User.objects.filter(username=form.cleaned_data["username"]).exists():
                form.add_error("username", "Username already exists. Try another.")
                return render(request, "register.html", {"form": form})

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"]
            )

            # Create the profile
            profile = Profile.objects.create(
                user=user,
                role=form.cleaned_data["role"],
                phone=form.cleaned_data["phone"],
                current_status=form.cleaned_data["current_status"],
                experience_years=form.cleaned_data["experience_years"] if form.cleaned_data["current_status"] == "experienced" else None
            )

            login(request, user)  # Auto-login after registration
            return redirect("home")  # Redirect to home page

    else:
        form = UserRegistrationForm()

    return render(request, "register.html", {"form": form})



def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.META.get('HTTP_REFERER', 'home'))  # Redirect to the previous page
        else:
            messages.error(request, "Invalid username or password.")
            return redirect(request.META.get('HTTP_REFERER', 'home'))  # Stay on the same page

    return redirect("home")  # Redirect if accessed directly

def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', 'home')) 


def Home(request):

    return render(request,"index.html")

def job_listing(request):
    return render(request,"job_listing.html")


def About(request):
    return render(request,"about.html")



def Contact(request):
    return render(request,"contact.html")

def blog(request):
    return render(request,"blog.html")

def elemen(request):
    return render(request,"elements.html")


def jobdetails(request):
    return render(request,"job_details.html")


def single_blog(request):
    return render(request,"single-blog.html")