from django.shortcuts import render, redirect
from .forms import *
from .models import *

def upload_file(request):
    if request.method == 'POST':
        form = AssignmentFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_success')  # Redirect after successful upload
    else:
        form = AssignmentFileForm()
    return render(request, 'upload.html', {'form': form})

def upload_success(request):
    return render(request, 'upload_success.html')

def file_list(request):
    files = AssignmentFile.objects.all()  # Get all uploaded files
    return render(request, 'file_list.html', {'files': files})

def upload_and_list_files(request):
    if request.method == 'POST':
        form = AssignmentFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_and_list')  # Redirect to the same view after uploading
    else:
        form = AssignmentFileForm()
        
    files = AssignmentFile.objects.all()  # Get all uploaded files
    return render(request, 'upload_and_list.html', {'form': form, 'files': files})
