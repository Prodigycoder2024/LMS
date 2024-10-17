# models.py

from django.db import models

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=[('Programming', 'Programming'), ('Science', 'Science')])
    description = models.TextField(blank=True)  # Make description optional
    prerequisites = models.CharField(max_length=255, blank=True)  # Make prerequisites optional
    due_date = models.DateField(null=True, blank=True)  # Make due_date optional


class Question(models.Model):
    text = models.TextField()
    subtitle = models.TextField(blank=True, null=True)
    question_type = models.CharField(max_length=50)
    answer_type = models.CharField(max_length=50)
    file_upload = models.FileField(upload_to='uploads/', blank=True, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)  # Assuming a relationship to Assignment