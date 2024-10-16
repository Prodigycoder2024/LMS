from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods


def upload_file(request):
    if request.method == 'POST':
        form = AssignmentFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_success')  # Redirect after successful upload
    else:
        form = AssignmentFileForm()
    return render(request, 'upload.html', {'form': form})

def upload_success(request):
    return render(request, 'upload_success.html')

def file_list(request):
    files = AssignmentFile.objects.all()  # Get all uploaded files
    return render(request, 'file_list.html', {'files': files})

def upload_and_list_files(request):
    if request.method == 'POST':
        form = AssignmentFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_and_list')  # Redirect to the same view after uploading
    else:
        form = AssignmentFileForm()
        
    files = AssignmentFile.objects.all()  # Get all uploaded files
    return render(request, 'upload_and_list.html', {'form': form, 'files': files})

# views.py

def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save()
            return redirect('add_questions', assignment_id=assignment.id)
    else:
        form = AssignmentForm()
    
    return render(request, 'create_assignment.html', {'form': form})


def add_questions(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.assignment = assignment
            
            # Handle options and correct answers
            if question_form.cleaned_data['question_type'] == 'multiple_choice':
                options = request.POST.getlist('options')
                correct_answers = request.POST.getlist('correct_answers')
                question.options = options
                question.correct_answers = correct_answers  # Store correct answers as a list
            
            question.save()
            return redirect('add_questions', assignment_id=assignment.id)
    else:
        question_form = QuestionForm()
    
    questions = Question.objects.filter(assignment=assignment)
    
    return render(request, 'add_questions.html', {'assignment': assignment, 'question_form': question_form, 'questions': questions})

@require_http_methods(["DELETE"])
def delete_question(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        question.delete()
        return JsonResponse({'success': True})
    except Question.DoesNotExist:
        return JsonResponse({'success': False}, status=404)

def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignment_list.html', {'assignments': assignments})