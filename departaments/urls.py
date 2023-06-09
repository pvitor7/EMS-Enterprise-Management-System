
from .views import DepartamentListCreateView, DepartamentRetrieveUpdateDestroyView, DepartamentEmployeeRetrieveUpdateDestroyView
from django.urls import path

urlpatterns = [
    path("departaments/", DepartamentListCreateView.as_view(), name="departament-list-create-view"),
    path("departaments/<pk>/", DepartamentRetrieveUpdateDestroyView.as_view(), name="departament-retrive-view"),
    path("departaments/<str:departament_id>/employees/<pk>/", DepartamentEmployeeRetrieveUpdateDestroyView.as_view(), name="departament-employee-retrive-view"),
]   