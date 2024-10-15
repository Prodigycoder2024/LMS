from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth import login
from django.contrib.auth import login as auth_login
from .forms import SignUpForm, LoginForm, AssignmentForm, SubmissionForm, GradeForm
from .models import InstructorData, Assignment, Submission, Grade

# User registration view
def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create the user object but don't save it yet
            user = form.save(commit=False)

            # Set the password manually
            password = form.cleaned_data.get('password1')
            user.set_password(password)
            user.save()

            # Handle role-specific data
            role = request.POST.get('role')
            if role == 'instructor':
                instructor_name = request.POST.get('instructorName')
                instructor_qualification = request.POST.get('instructorQualification')

                # Save the instructor-specific data
                InstructorData.objects.create(
                    user=user,
                    instructorName=instructor_name,
                    instructorQualification=instructor_qualification
                )

            # Authenticate the user
            authenticated_user = authenticate(username=user.username, password=password)
            if authenticated_user is not None:
                # Log the user in if authentication is successful
                login(request, authenticated_user)
                return redirect('dashboard')  # Ensure 'home' is defined in your URLs
            else:
                # Handle the case where authentication fails (unlikely but good practice)
                print("Authentication failed")
        else:
            # Print form errors if the form is invalid
            print("Form is not valid", form.errors)
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
                return redirect('dashboard')  # Redirect to dashboard or desired page
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

# Create assignment view (Updated)
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
    print(form['category'])
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

# Create submission view (for a specific assignment)
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

# Submission list (empty view placeholder)
@login_required
def submission_list(request):
    submissions = Submission.objects.filter(student=request.user)
    return render(request, 'assignments/submission_list.html', {'submissions': submissions})

def save_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, 'Assignment saved successfully!')  # Add a success message
            return redirect('assignment_list')  
    else:
        form = AssignmentForm()  # Create an empty form instance
