from django import forms
from core.models import TimeLog, Task


class TimeLogForm(forms.ModelForm):
    class Meta:
        model = TimeLog
        fields = ['task', 'hours_spent', 'date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task'].queryset = Task.objects.all()  #show all tasks in dropdown