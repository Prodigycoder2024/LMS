from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Assignment, Submission, Grade, InstructorData, User

# Form for creating assignments
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']

# Form for submitting assignments (includes assignment selection)
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['assignment', 'submitted_file']

# Form for grading assignments (includes submission selection)
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['submission', 'score', 'feedback']

# Form for instructor data
class InstructorDataForm(forms.ModelForm):
    class Meta:
        model = InstructorData
        fields = ['instructorName', 'instructorQualification']

# Login form for user authentication
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )

# Sign-up form for user registration
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
