from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import *
from django.contrib import admin
from django.urls import path, include
from courses_details import views

urlpatterns = [

    # other url patterns

    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('admin/', admin.site.urls),
    # path('', include('courses_details.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),  # Add this line

    # Assignment-related URLs
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/create/', create_assignment, name='create_assignment'),
    path('assignments/<int:assignment_id>/submit/', views.create_submission, name='create_submission'),
    
    # Submission-related URLs
    path('submissions/', views.submission_list, name='submission_list'),
    path('submissions/<int:submission_id>/grade/', views.grade_submission, name='grade_submission'),

    # Grades
    path('grades/', views.grade_list, name='grade_list'),

    # Other views
    path('', views.home, name='home'),
    path('my_courses/', views.my_courses, name='my_courses'),
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('instructor/', views.instructor, name='instructor'),
    path('profile/', views.profile, name='profile'),
    path('admin/', views.admin_panel, name='admin'),

    # Authentication-related URLs
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('reset-password/', views.reset_password_view, name='reset_password'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]
