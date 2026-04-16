from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from core.models import Project, Bug, Module, User , Task, TimeLog
from django.db import models

# Create your views here.
#@login_required(login_url="login")
@role_required(allowed_roles=["admin"])
def adminDashboardView(request):
    projects = Project.objects.all()
    total_projects = projects.count()
    total_users = User.objects.count()
    total_tasks = Task.objects.count()
    total_bugs = Bug.objects.count()
    recent_bugs = Bug.objects.order_by('-reported_date')[:5]

    for project in projects:
        project.total_tasks = Task.objects.filter(module__project=project).count()

    return render(request, "dashboards/admin_dashboard.html", {'projects': projects,'total_projects': total_projects,'total_users': total_users,'total_tasks': total_tasks,'total_bugs': total_bugs,'recent_bugs': recent_bugs,})

#@login_required(login_url="login")
@role_required(allowed_roles=["manager"])
def managerDashboardView(request):
    projects = Project.objects.filter(manager=request.user)
    my_projects = projects.count()
    total_modules = Module.objects.filter(project__manager=request.user).count()
    total_tasks = Task.objects.filter(module__project__manager=request.user).count()
    total_bugs = Bug.objects.filter(task__module__project__manager=request.user).count()
    pending_tasks = Task.objects.filter(module__project__manager=request.user, status='Pending').count()

    for project in projects:
        project.total_tasks = Task.objects.filter(module__project=project).count()
        project.pending_tasks = Task.objects.filter(module__project=project, status='Pending').count()

    return render(request, "dashboards/manager_dashboard.html",{'projects': projects,'my_projects': my_projects,'total_modules': total_modules,'total_tasks': total_tasks,'total_bugs': total_bugs,'pending_tasks': pending_tasks,})

#@login_required(login_url="login")
@role_required(allowed_roles=["developer"])
def developerDashboardView(request):
    assigned_tasks = Task.objects.filter(assigned_to=request.user)
    total_tasks = assigned_tasks.count()
    total_bugs = Bug.objects.filter(assigned_to=request.user).count()
    #total_timelogs = TimeLog.objects.filter(developer=request.user).count()
    total_hours = TimeLog.objects.filter(developer=request.user).aggregate(total=models.Sum('hours_spent'))['total'] or 0
    pending_tasks = assigned_tasks.filter(status='Pending').count()
    return render(request, "dashboards/developer_dashboard.html", {'assigned_tasks': assigned_tasks,'total_tasks': total_tasks,'total_bugs': total_bugs,'pending_tasks': pending_tasks,'total_hours': total_hours,})

#@login_required(login_url="login")
@role_required(allowed_roles=["tester"])
def testerDashboardView(request):
    reported_bugs = Bug.objects.filter(reported_by=request.user)
    total_bugs = reported_bugs.count()
    pending_bugs = reported_bugs.filter(status='Pending').count()
    resolved_bugs = reported_bugs.filter(status='Completed').count()
    tasks_to_test = Task.objects.filter(status='Completed').count()
    return render(request,"dashboards/tester_dashboard.html",{'reported_bugs': reported_bugs,'total_bugs': total_bugs,
            'pending_bugs': pending_bugs,'resolved_bugs': resolved_bugs,'tasks_to_test': tasks_to_test,})