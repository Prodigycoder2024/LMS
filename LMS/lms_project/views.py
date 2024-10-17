from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from .models import Question 
from .forms import *
from .models import *

def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            # Create an Assignment instance
            assignment = Assignment(
                title=form.cleaned_data['title'],
                category=form.cleaned_data['category'],
                description=form.cleaned_data['description'],
                prerequisites=form.cleaned_data['prerequisites'],
                due_date=form.cleaned_data['due_date']
            )
            assignment.save()  # Save the assignment to the database

            # Redirect to the add_questions page with the assignment title
            return redirect('add_questions', assignment_title=assignment.title)  # Pass the title here
    else:
        form = AssignmentForm()

    return render(request, 'create_assignment.html', {'form': form})

def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignments/assignment_list.html', {'assignments': assignments})

def add_questions(request, assignment_title):
    # Pass the assignment_title to the template
    context = {
        'assignment_title': assignment_title,
        'questions': Question.objects.filter(assignment__title=assignment_title),  # Fetch questions related to this assignment
    }
    return render(request, 'add_questions.html', context)

def submit_questions(request, assignment_title):
    # Fetch the assignment object using the title
    assignment = get_object_or_404(Assignment, title=assignment_title)

    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        subtitle = request.POST.get('subtitle')
        question_type = request.POST.get('question_type')
        answer_type = request.POST.get('answer_type')
        file_upload = request.FILES.get('file_upload')

        # Save the question to the database
        question = Question.objects.create(
            text=question_text,
            subtitle=subtitle,
            question_type=question_type,
            answer_type=answer_type,
            file_upload=file_upload,
            assignment=assignment  # Associate the question with the assignment
        )

        return redirect('add_questions', assignment_title=assignment_title)  # Redirect back to the add_questions page

    # To display previously uploaded files if applicable
    questions = Question.objects.filter(assignment=assignment)

    return render(request, 'add_questions.html', {
        'assignment_title': assignment_title,
        'questions': questions,  # Pass uploaded questions to the template
    })

def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        question.file_upload.delete(save=False)  # Delete the file from the filesystem
        question.delete()  # Delete the question from the database
        return redirect('add_questions', assignment_title=question.assignment.title)  # Redirect to add_questions with the assignment title

    return redirect('add_questions', assignment_title=question.assignment.title)  # Redirect if the request is not POST

def fetch_questions(request, assignment_title):
    questions = Question.objects.filter(assignment__title=assignment_title)  # Adjust the query as needed
    return render(request, 'fetch_questions.html', {
        'assignment_title': assignment_title,
        'questions': questions,
    })