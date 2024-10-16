from django import forms
from .models import AssignmentFile,Assignment, Question

class AssignmentFileForm(forms.ModelForm):
    class Meta:
        model = AssignmentFile
        fields = ['title', 'file', 'description', 'due_date']
    


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'category', 'description', 'prerequisites', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control title-input'}),
            'category': forms.Select(attrs={'class': 'form-control category-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control description-textarea'}),
            'prerequisites': forms.TextInput(attrs={'class': 'form-control prerequisites-input'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control due-date-input', 'type': 'date'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['description'].required = False
            self.fields['prerequisites'].required = False
            self.fields['due_date'].required = False

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'subtitle', 'question_type', 'answer_type']
        widgets = {
            'subtitle': forms.TextInput(attrs={'class': 'form-control subtitle-input', 'placeholder': 'Subtitle'}),
            'question_text': forms.TextInput(attrs={'class': 'form-control question-text-input', 'rows': 2, 'placeholder': 'Question Text'}),
            'question_type': forms.Select(attrs={'class': 'form-control question-type-select'}),
            'answer_type': forms.Select(attrs={'class': 'form-control answer-type-select'}),
        }
