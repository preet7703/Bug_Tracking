from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.taskListView, name='task_list'),
    path('create/', views.taskCreateView, name='task_create'),
    path('<int:id>/detail/', views.taskDetailView, name='task_detail'),
    path('<int:id>/edit/', views.taskEditView, name='task_edit'),
    path('<int:id>/delete/', views.taskDeleteView, name='task_delete'),
]