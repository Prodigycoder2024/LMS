from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, get_user_model
from .forms import SignUpForm, LoginForm, AssignmentForm, SubmissionForm, GradeForm
from .models import InstructorData, Assignment, Submission, Grade

# User registration view
def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = request.POST.get('role')
            if role == 'instructor':
                instructor_name = request.POST.get('instructorName')
                instructor_qualification = request.POST.get('instructorQualification')
                InstructorData.objects.create(
                    user=user,
                    instructorName=instructor_name,
                    instructorQualification=instructor_qualification
                )
            user = authenticate(username=user.username, password=request.POST.get('password1'))
            if user is not None:
                auth_login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'login/register.html', {'form': form})

# User login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})

# Reset password view
def reset_password_view(request):
    User = get_user_model()
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'User not found. Please enter a valid username.')
    return render(request, 'login/reset_password.html')

# Home page view
def home(request):
    return render(request, 'courses_details/home.html')

# Dashboard view
@login_required
def dashboard(request):
    return render(request, 'courses_details/dashboard.html')

# Courses view
@login_required
def my_courses(request):
    return render(request, 'courses_details/my_courses.html')

# Instructor view
@login_required
def instructor(request):
    return render(request, 'courses_details/instructor.html')

# Contact us view
def contact_us(request):
    return render(request, 'courses_details/contact_us.html')

# About us view
def about_us(request):
    return render(request, 'courses_details/about_us.html')

# Profile view
@login_required
def profile(request):
    return render(request, 'courses_details/profile.html')

# Admin panel view
@login_required
def admin_panel(request):
    return render(request, 'courses_details/admin.html')

# Assignment list view
@login_required
def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'courses_details/assignment_list.html', {'assignments': assignments})

# Create assignment view
@login_required
def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.created_by = request.user
            assignment.save()
            messages.success(request, 'Assignment created successfully.')
            return redirect('assignment_list')
    else:
        form = AssignmentForm()
    return render(request, 'courses_details/assignment_form.html', {'form': form})

# Submit assignment view
@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            return redirect('assignment_list')
    else:
        form = SubmissionForm()
    return render(request, 'courses_details/submit_assignment.html', {'form': form, 'assignment': assignment})

# Grade submission view
@login_required
def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.submission = submission
            grade.save()
            messages.success(request, 'Submission graded successfully.')
            return redirect('assignment_list')
    else:
        form = GradeForm()
    return render(request, 'courses_details/grade_submission.html', {'form': form, 'submission': submission})

# Grade list view
@login_required
def grade_list(request):
    grades = Grade.objects.filter(submission__student=request.user)
    return render(request, 'grades/grade_list.html', {'grades': grades})

# Create submission view
@login_required
def create_submission(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.assignment = assignment
            submission.save()
            messages.success(request, 'Submission created successfully.')
            return redirect('submission_list')
    else:
        form = SubmissionForm()
    return render(request, 'assignments/submit_assignment.html', {'form': form, 'assignment': assignment})

def submission_list():
    pass