from django.urls import path
from . import views

urlpatterns = [
    path("adminDashboard/",views.adminDashboardView,name="adminDashboard"),
    path("managerDashboard/",views.managerDashboardView,name="managerDashboard"),
    path("testerDashboard/",views.testerDashboardView,name="testerDashboard"),
    path("developerDashboard/",views.developerDashboardView,name="developerDashboard"),
]