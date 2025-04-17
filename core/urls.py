from django.urls import path
from . import views

urlpatterns = [
    # Home and Logout
    path('', views.home, name='home'),
    path('logout/', views.user_logout, name='logout'),

    # User Registration & Login
    path('candidate/register/', views.candidate_register, name='candidate_register'),
    path('recruiter/register/', views.recruiter_register, name='recruiter_register'),
    path('login/', views.user_login, name='login'),

    # Candidate Views
    path('candidate/dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('candidate/profile/', views.candidate_profile, name='candidate_profile'),
    path('candidate/profile/update/', views.update_candidate_profile, name='update_candidate_profile'),

    # Recruiter Views
    path('recruiter/dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('recruiter/create-job/', views.create_job, name='create_job'),
    path('recruiter/job/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('recruiter/job/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),
    path('recruiter/candidate/<int:candidate_id>/', views.view_candidate_profile, name='view_candidate_profile'),
    path('recruiter/update_profile/', views.update_recruiter_profile, name='update_recruiter_profile'),
    path('company/<int:recruiter_id>/', views.company_profile, name='company_profile'),


    # Job-related Views
    path('job/<int:job_id>/', views.job_details, name='job_details'),
    path('job/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('job/<int:job_id>/save/', views.save_job, name='save_job'),
    path('job/<int:job_id>/unsave/', views.unsave_job, name='unsave_job'),


    path('dashboard/', views.dashboard_redirect, name='user_dashboard'),
    path('aboutus/',views.aboutus,name='about_us'),
    path('Carrers/',views.Careers,name='Careers'),
    path('career-tips/', views.career_tips, name='career_tips'),
    path('privacypolicy/', views.privacypoliccy, name='pp'),
    path('TermsofServices/', views.ts, name='TOS'),
    path('job/update/<int:job_id>/', views.update_job, name='update_job'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<int:user_id>/', views.reset_password, name='reset_password'),






    # Error Handling (Optional if you added a custom 404 page)
    # path('404/', views.custom_404, name='custom_404'),
]
