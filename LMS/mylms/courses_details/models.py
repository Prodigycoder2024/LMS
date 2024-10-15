from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from datetime import timedelta


# Custom user model
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=True)
    is_instructor = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# Instructor data model
class InstructorData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_data', null=True, blank=True)
    instructorName = models.CharField(max_length=255)
    instructorQualification = models.CharField(max_length=255)

    def __str__(self):
        return self.instructorName 
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Assignment model
class Assignment(models.Model):
    title = models.CharField(max_length=200)
    category =models.ForeignKey(Category, on_delete=models.CASCADE, related_name='assignments')  # Dropdown field
    prerequisites = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField(default=timezone.now() + timedelta(days=7))  # Default to 7 days from now
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')

    def __str__(self):
        return self.title

# Submission model
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_file = models.FileField(upload_to='submissions/')
    submission_date = models.DateTimeField(auto_now_add=True)  # Auto set to now on creation

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

# Grade model
class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE)
    score = models.IntegerField()
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.submission.student.username} - {self.score}"