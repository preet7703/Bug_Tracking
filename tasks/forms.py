from django import forms
from core.models import Task, Module, User


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'module', 'assigned_to', 'status', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # only show developers in assigned_to dropdown
        self.fields['assigned_to'].queryset = User.objects.filter(role='developer')
        # show all modules in dropdown
        self.fields['module'].queryset = Module.objects.all()