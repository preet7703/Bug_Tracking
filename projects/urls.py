from django.urls import path
from . import views

urlpatterns = [
    #Project Urls 
    path('project/list/', views.projectListView, name='project_list'),
    path('project/create/', views.projectCreateView, name='project_create'),
    path('project/<int:id>/detail/', views.projectDetailView, name='project_detail'),
    path('project/<int:id>/edit/', views.projectEditView, name='project_edit'),
    path('project/<int:id>/delete/', views.projectDeleteView, name='project_delete'),
    #Module Urls 
    path('module/list/', views.moduleListView, name='module_list'),
    path('module/create/', views.moduleCreateView, name='module_create'),
    path('module/<int:id>/edit/', views.moduleEditView, name='module_edit'),
    path('module/<int:id>/delete/', views.moduleDeleteView, name='module_delete'),

    
]