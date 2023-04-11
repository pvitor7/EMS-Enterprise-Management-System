
from .views import EmployeeListCreateView, EmployeeRetrieveUpdateDestroyView
from django.urls import path

urlpatterns = [
    path("", EmployeeListCreateView.as_view(), name="departament-list-create-view"),
    path("<pk>/", EmployeeRetrieveUpdateDestroyView.as_view(), name="departament-retrive-view"),
]   