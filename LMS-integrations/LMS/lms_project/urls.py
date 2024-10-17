# urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('', views.create_assignment, name='create_assignment'),
    path('add_questions/<str:assignment_title>/', views.add_questions, name='add_questions'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('submit_questions/<str:assignment_title>/', views.submit_questions, name='submit_questions'),  # Ensure this is defined
    path('fetch_questions/<str:assignment_title>/', views.fetch_questions, name='fetch_questions'),  # Add this line
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
