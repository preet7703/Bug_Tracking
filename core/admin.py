from django.contrib import admin
from .models import User,Project, Module, Task, Bug, TimeLog

# Register your models here.

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Module)
admin.site.register(Task)
admin.site.register(Bug)
admin.site.register(TimeLog)
