from django import forms
from .models import AssignmentFile

class AssignmentFileForm(forms.ModelForm):
    class Meta:
        model = AssignmentFile
        fields = ['title', 'file']
    