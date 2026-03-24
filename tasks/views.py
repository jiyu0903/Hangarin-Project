from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from .models import Task
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

@login_required
def home(request):
    all_tasks = Task.objects.all()

    stats = {
        'total': all_tasks.count(),
        'pending': all_tasks.filter(status="Pending").count(),
        'in_progress': all_tasks.filter(status="In Progress").count(),
        'completed': all_tasks.filter(status="Completed").count(),
    }

    tasks = all_tasks

    # Filter by status
    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)

    # Search by query
    q = request.GET.get('q')
    if q:
        tasks = tasks.filter(Q(title__icontains=q) | Q(description__icontains=q))

    return render(request, 'tasks/home.html', {
        'tasks': tasks,
        'stats': stats
    })

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'tasks/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def add_task(request):
    if request.method == 'POST':
        Task.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            status=request.POST['status'],
            deadline=request.POST['deadline'],
            priority_id=request.POST['priority'],
            category_id=request.POST['category']
        )
        return redirect('home')

    return render(request, 'tasks/add_task.html')

def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()
    return redirect('home')

def edit_task(request, id):
    task = get_object_or_404(Task, id=id)

    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.status = request.POST['status']
        task.save()
        return redirect('home')

    return render(request, 'tasks/edit_task.html', {'task': task})