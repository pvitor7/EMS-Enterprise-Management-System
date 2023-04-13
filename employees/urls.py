
from .views import EmployeeListCreateView, EmployeeRetrieveUpdateDestroyView, DepartamentEmployeeView, DepartamentEmployeeIDView
from django.urls import path

urlpatterns = [
    path("employees/<pk>/", EmployeeRetrieveUpdateDestroyView.as_view()),
    path("employees/", EmployeeListCreateView.as_view()),
    path("departaments/<str:departament_id>/employees/", DepartamentEmployeeView.as_view()),
    path("departaments/<str:departament_id>/employees/<pk>/", DepartamentEmployeeIDView.as_view()),
]   