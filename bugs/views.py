from django.shortcuts import render, redirect, get_object_or_404
from core.models import Bug, Task, User, Module, Project
from .forms import BugForm
from dashboards.decorators import role_required

# Create your views here.
@role_required(allowed_roles=['admin','manager','developer','tester'])
def bugListView(request):
    if request.user.role =='admin':
        bugs = Bug.objects.all()
    elif request.user.role =='manager':
        bugs = Bug.objects.filter(task__module__project__manager=request.user)
    elif request.user.role=='developer':
        bugs = Bug.objects.filter(assigned_to=request.user)
    else:
        bugs = Bug.objects.filter(reported_by=request.user) # tester sees bugs they reported
    return render(request,'bugs/bug_list.html',{'bugs':bugs})


@role_required(allowed_roles=['admin','manager','tester'])
def bugCreateView(request):
    if request.method =='POST':
        form = BugForm(request.POST)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.reported_by = request.user
            bug.save()
            return redirect('bug_list')
        else:
            tasks = Task.objects.all()
            developers = User.objects.filter(role='developer')
            return render(request,'bugs/bug_create.html',{'form':form,'tasks':tasks,'developers':developers})
    else:
        form = BugForm()
        tasks = Task.objects.all()
        developers = User.objects.filter(role='developer')
        return render(request,'bugs/bug_create.html',{'form':form,'tasks':tasks,'developers': developers})


@role_required(allowed_roles=['admin','manager','developer','tester'])
def bugDetailView(request, id):
    bug = get_object_or_404(Bug, id=id)
    return render(request,'bugs/bug_detail.html',{'bug':bug})


@role_required(allowed_roles=['admin', 'manager'])
def bugEditView(request, id):
    bug = get_object_or_404(Bug, id=id)
    if request.method == 'POST':
        form = BugForm(request.POST, instance=bug)
        if form.is_valid():
            form.save()
            return redirect('bug_list')
        else:
            tasks = Task.objects.all()
            developers = User.objects.filter(role='developer')
            return render(request, 'bugs/bug_edit.html', {'form': form,'bug': bug,'tasks': tasks,'developers': developers,
                'selected_task': str(bug.task.id),
                'selected_developer': str(bug.assigned_to.id) if bug.assigned_to else '',
            })
    else:
        form = BugForm(instance=bug)
        tasks = Task.objects.all()
        developers = User.objects.filter(role='developer')
        return render(request,'bugs/bug_edit.html',{'form': form,'bug': bug,'tasks': tasks,'developers': developers,
            'selected_task': str(bug.task.id),
            'selected_developer': str(bug.assigned_to.id) if bug.assigned_to else '',
        })

@role_required(allowed_roles=['admin','manager'])
def bugDeleteView(request, id):
    bug = get_object_or_404(Bug,id=id)
    if request.method == 'POST':
        bug.delete()
        return redirect('bug_list')
    return render(request,'bugs/bug_delete.html',{'bug': bug})

@role_required(allowed_roles=['admin', 'manager','developer','tester'])
def bugUpdateStatusView(request, id):
    bug = get_object_or_404(Bug, id=id)
    if request.method == 'POST':
        bug.status = request.POST.get('status')
        bug.save()
    return redirect('bug_detail',id=bug.id)