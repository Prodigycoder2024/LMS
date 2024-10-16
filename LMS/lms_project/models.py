from django.db import models
from django.contrib.auth.models import User

class AssignmentFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    description = models.CharField(max_length=500)
    due_date = models.DateTimeField()  # Field for the due date
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who created the assignment

    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class Assignment(models.Model):
    TITLE_CATEGORIES = [
        ('Programming', 'Programming'),
        ('Mathematics', 'Mathematics'),
        ('Science', 'Science'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=TITLE_CATEGORIES)
    description = models.TextField(blank=True, null=True)
    prerequisites = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('text', 'Text Input'),
        ('upload', 'File Upload'),
    ]
    
    ANSWER_TYPES = [
        ('single', 'Single Choice'),
        ('multiple', 'Multiple Answers'),
    ]

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    subtitle = models.CharField(max_length=200, blank=True)
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    answer_type = models.CharField(max_length=20, choices=ANSWER_TYPES, default='single')
    options = models.JSONField(blank=True, null=True)  # Store options as a list in JSON format
    correct_answers = models.JSONField(blank=True, null=True)  # Store correct answers as a list

    def __str__(self):
        return self.question_text
