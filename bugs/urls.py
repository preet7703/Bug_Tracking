from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.bugListView, name='bug_list'),
    path('create/', views.bugCreateView, name='bug_create'),
    path('<int:id>/detail/', views.bugDetailView, name='bug_detail'),
    path('<int:id>/edit/', views.bugEditView, name='bug_edit'),
    path('<int:id>/delete/', views.bugDeleteView, name='bug_delete'),
    path('<int:id>/update-status/', views.bugUpdateStatusView, name='bug_update_status'),
]