from django.shortcuts import render, redirect, get_object_or_404
from core.models import Project, Module, User, Task
from .forms import ProjectForm, ModuleForm
from dashboards.decorators import role_required

# Create your views here.

#Project View:-

@role_required(allowed_roles=['admin','manager'])
def projectListView(request):
    if request.user.role == 'admin':
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(manager=request.user)
    return render(request, 'projects/project_list.html', {'projects': projects})


@role_required(allowed_roles=['admin','manager'])
def projectCreateView(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
        else:
            return render(request,'projects/project_create.html',{'form': form})
    else:
        form = ProjectForm()
        return render(request,'projects/project_create.html',{'form': form})


@role_required(allowed_roles=['admin','manager'])
def projectDetailView(request, id):
    project = get_object_or_404(Project, id=id)
    modules = Module.objects.filter(project=project)
    tasks = Task.objects.filter(module__project=project) 
    return render(request,'projects/project_detail.html',{'project': project, 'modules': modules, 'tasks': tasks})


@role_required(allowed_roles=['admin','manager'])
def projectEditView(request, id):
    project = get_object_or_404(Project,id=id)
    if request.method == 'POST':
        form = ProjectForm(request.POST,instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
        else:
            return render(request,'projects/project_edit.html',{'form': form,'project': project,'selected_manager': str(project.manager.id),})
    else:
        form = ProjectForm(instance=project)
        return render(request,'projects/project_edit.html',{'form': form,'project': project,'selected_manager': str(project.manager.id),})


@role_required(allowed_roles=['admin','manager'])
def projectDeleteView(request, id):
    project = get_object_or_404(Project,id=id)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request,'projects/project_delete.html',{'project': project})

#Modul View:-

@role_required(allowed_roles=['admin','manager'])
def moduleListView(request):
    modules = Module.objects.all()
    return render(request,'projects/module_list.html',{'modules': modules})


@role_required(allowed_roles=['admin', 'manager'])
def moduleCreateView(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('module_list')
        else:
            projects = Project.objects.all()
            return render(request,'projects/module_create.html',{'form': form, 'projects': projects})
    else:
        form = ModuleForm()
        projects = Project.objects.all()
        return render(request,'projects/module_create.html', {'form': form,'projects': projects})


@role_required(allowed_roles=['admin', 'manager'])
def moduleEditView(request, id):
    module = get_object_or_404(Module, id=id)
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('module_list')
        else:
            projects = Project.objects.all()
            return render(request,'projects/module_edit.html',{'form': form,'module': module,'projects': projects,
                'selected_project': str(module.project.id),
            })
    else:
        form = ModuleForm(instance=module)
        projects = Project.objects.all()
        return render(request,'projects/module_edit.html',{'form': form,'module': module,'projects': projects,
            'selected_project': str(module.project.id),
        })


@role_required(allowed_roles=['admin','manager'])
def moduleDeleteView(request, id):
    module = get_object_or_404(Module,id=id)
    if request.method == 'POST':
        module.delete()
        return redirect('module_list')
    return render(request,'projects/module_delete.html', {'module': module})