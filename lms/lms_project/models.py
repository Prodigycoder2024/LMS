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
