from django.urls import path
from django.conf.urls.static import static
from . import views
from .views import *
from django.conf import settings

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('upload_and_list', views.upload_and_list_files, name='upload_and_list'),
    path('upload/success/', views.upload_success, name='upload_success'),
    path('files/', views.file_list, name='file_list'),
    path('', create_assignment, name='create_assignment'),
    path('add-questions/<int:assignment_id>/', add_questions, name='add_questions'),
    path('delete-question/<int:question_id>/', delete_question, name='delete_question'),
    path('assignments/', assignment_list, name='assignment_list'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)