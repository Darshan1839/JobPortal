from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name="home"),
    path('FindJobs/',job_listing,name="FJ"),
    path("About/",About,name="AB"),
    path("contact/",Contact,name="contact"),
    path("blog/",blog,name="blog"),
    path("elements/",elemen,name="elem"),
    path("job_details/",jobdetails,name="jd"),
    path("blog_details/",single_blog,name="sb"),
    path("register/", register, name="register"),

    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),

]
