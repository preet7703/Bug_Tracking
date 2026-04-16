from django import forms
from core.models import Project, Module, User


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name','description','manager']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # only show managers in dropdown,
        # without this line, all users (admin, developer, tester) will appear in dropdown
        self.fields['manager'].queryset = User.objects.filter(role='manager')


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['project','name']