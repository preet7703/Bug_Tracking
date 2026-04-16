from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.timelogListView, name='timelog_list'),
    path('create/', views.timelogCreateView, name='timelog_create'),
    path('<int:id>/detail/', views.timelogDetailView, name='timelog_detail'),
    path('<int:id>/delete/', views.timelogDeleteView, name='timelog_delete'),
]