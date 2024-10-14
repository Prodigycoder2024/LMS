from courses_details import views
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import assignment_list, submit_assignment, grade_submission, create_assignment

urlpatterns = [
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
