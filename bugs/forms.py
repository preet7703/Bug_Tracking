from django import forms
from core.models import Bug, Task, User, Module, Project


class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['task', 'description', 'assigned_to', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # only show developers in assigned_to dropdown
        self.fields['assigned_to'].queryset = User.objects.filter(role='developer')
        # show all tasks in dropdown
        self.fields['task'].queryset = Task.objects.all()