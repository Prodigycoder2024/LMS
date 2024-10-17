from django import forms
from .models import *

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'category', 'description', 'prerequisites', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'category': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prerequisites': forms.TextInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class QuestionForm(forms.Form):
    question_text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    subtitle = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    question_type = forms.ChoiceField(
        choices=[('MCQ', 'Multiple Choice'), ('Text Input', 'Text Input'), ('File Upload', 'File Upload')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    answer_type = forms.ChoiceField(
        choices=[('Single', 'Single Choice'), ('Multiple', 'Multiple Choice')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    file_upload = forms.FileField(required=False)   # File upload field