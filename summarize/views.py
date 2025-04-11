from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
import os

from .models import Submission
from .forms import sumForm
from .functions import handle_uploaded_files, query_llm

def index(request: HttpRequest) -> HttpResponse:
    """
    Generate the home page for the project

    Args:
        request (HttpRequest): the HTTP request received

    Returns:
        HttpResponse: the response given
    """
    
    submissions = Submission.objects.all().order_by('-date')
    summary = ""
    title = ""
    show = False
    
    # If there are submissions, get the latest one
    if submissions.exists():
        latest = submissions.first()
        summary = latest.summary
        title = latest.title
    
    # If the form is submitted and valid, it will be saved to the database
    if request.method == "POST":
        show = True
        form = sumForm(request.POST, request.FILES)
        if form.is_valid():
            model_instance = form.save()
            messages.success(request, "File uploaded successfully!")
            return redirect('result')
        else:
            messages.error(request, "An error occurred while uploading the file!")
    
    # Otherwise, a new form will be instantiated
    form = sumForm()
    
    # Preparing the context to pass to the template
    context = {
        "forms": form,
        "summary": summary,
        "title": title,
        "show": show,
        "submissions": submissions
    }
    
    return render(request, 'index.html', context)

def summary(request: HttpRequest) -> HttpResponse:
    """
    Generate the summary and populate the respective text field

    Args:
        request (HttpRequest): the HTTP request received

    Returns:
        HttpResponse: the response given
    """
    
    query = Submission.objects.last()
    title = query.title
    
    query.summary = query_llm()
    summary = query.summary
    query.save()
    
    form = sumForm()
    submissions = Submission.objects.all().order_by('-date')
    
    # Preparing the context to pass to the template
    context = {
        "forms": form,
        "summary": summary,
        "title": title,
        "show": True,
        "submissions": submissions
    }
    
    return render(request, 'index.html', context)

# CRUD Operations
def submission_list(request):
    """Display the list of uploaded files"""
    submissions = Submission.objects.all().order_by('-date')
    return render(request, 'submission_list.html', {'submissions': submissions})

def submission_detail(request, pk):
    """Display details of a specific file"""
    submission = get_object_or_404(Submission, pk=pk)
    return render(request, 'submission_detail.html', {'submission': submission})

def submission_edit(request, pk):
    """Edit an existing file"""
    submission = get_object_or_404(Submission, pk=pk)
    if request.method == "POST":
        form = sumForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            # If the file is changed, delete the old file
            if 'paper' in request.FILES:
                if submission.paper and os.path.isfile(submission.paper.path):
                    os.remove(submission.paper.path)
            
            form.save()
            messages.success(request, "File updated successfully!")
            return redirect('submission_detail', pk=submission.pk)
    else:
        form = sumForm(instance=submission)
    return render(request, 'submission_edit.html', {'form': form})

def submission_delete(request, pk):
    """Delete an existing file"""
    submission = get_object_or_404(Submission, pk=pk)
    if request.method == "POST":
        # Delete the file from the file system
        if submission.paper and os.path.isfile(submission.paper.path):
            os.remove(submission.paper.path)
        
        submission.delete()
        messages.success(request, "File deleted successfully!")
        return redirect('submission_list')
    return render(request, 'submission_confirm_delete.html', {'submission': submission})

def submission_create(request):
    """Create a new file"""
    if request.method == "POST":
        form = sumForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save()
            messages.success(request, "New file created successfully!")
            return redirect('submission_detail', pk=submission.pk)
    else:
        form = sumForm()
    return render(request, 'submission_create.html', {'form': form})