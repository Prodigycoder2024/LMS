from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [
    path('upload', views.upload_file, name='upload_file'),
    path('', views.upload_and_list_files, name='upload_and_list'),
    path('upload/success/', views.upload_success, name='upload_success'),
    path('files/', views.file_list, name='file_list'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)