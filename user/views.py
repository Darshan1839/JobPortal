from django.shortcuts import render,redirect

# Create your views here.


from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import UserRegistrationForm

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )
            user.profile.role = form.cleaned_data["role"]
            user.profile.phone = form.cleaned_data["phone"]
            user.profile.save()
            
            login(request, user)  # Auto-login after registration
            return redirect("home")  # Redirect to the home page

    else:
        form = UserRegistrationForm()

    return render(request, "register.html", {"form": form})



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