from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from todoApp.models import Task


# Create your views here.
@login_required(login_url='login')
def index(request):
    tasks = []
    if request.user:
        tasks = Task.objects.filter(owner=request.user, parent__isnull=True)

    return render(request, "index.html", context={'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        title       = request.POST.get('title','').strip()
        description = request.POST.get('description','').strip()
        due_date    = request.POST.get('due_date') or None
        parent_id   = request.POST.get('task_id')

        parent = None
        if parent_id:
            parent = get_object_or_404(Task, pk=parent_id)

        Task.objects.create(
            title       = title,
            description = description,
            due_date    = due_date,
            parent      = parent,
            owner       = request.user,
        )

    return redirect('index')

def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if task.parent is None:
        task.subtasks.all().delete()

    task.delete()

    return redirect('index')