from django.shortcuts import render, redirect, get_object_or_404
from core.models import TimeLog, Task, User
from .forms import TimeLogForm
from dashboards.decorators import role_required

# Create your views here.
@role_required(allowed_roles=['admin','manager','developer'])
def timelogListView(request):
    if request.user.role == 'admin':
        timelogs = TimeLog.objects.all()
    elif request.user.role == 'manager':
        timelogs = TimeLog.objects.filter(task__module__project__manager=request.user)
    else:
        # developer sees only their own timelogs
        timelogs = TimeLog.objects.filter(developer=request.user)
    return render(request,'timelogs/timelog_list.html',{'timelogs': timelogs})


@role_required(allowed_roles=['admin','developer'])
def timelogCreateView(request):
    if request.method == 'POST':
        form = TimeLogForm(request.POST)
        if form.is_valid():
            timelog = form.save(commit=False)
            timelog.developer = request.user
            timelog.save()
            return redirect('timelog_list')
        else:
            tasks = Task.objects.filter(assigned_to=request.user) if request.user.role == 'developer' else Task.objects.all()
            return render(request,'timelogs/timelog_create.html',{'form':form,'tasks': tasks})
    else:
        form = TimeLogForm()
        tasks = Task.objects.filter(assigned_to=request.user) if request.user.role == 'developer' else Task.objects.all()
        return render(request,'timelogs/timelog_create.html',{'form': form, 'tasks': tasks})


@role_required(allowed_roles=['admin','manager','developer'])
def timelogDetailView(request, id):
    timelog = get_object_or_404(TimeLog, id=id)
    return render(request,'timelogs/timelog_detail.html',{'timelog': timelog})


@role_required(allowed_roles=['admin'])
def timelogDeleteView(request, id):
    timelog = get_object_or_404(TimeLog, id=id)
    if request.method == 'POST':
        timelog.delete()
        return redirect('timelog_list')
    return render(request,'timelogs/timelog_delete.html',{'timelog': timelog})
