
from .views import EmployeeListCreateView, EmployeeRetrieveUpdateDestroyView, DepartamentEmployeeView, DepartamentEmployeeIDView, ProjectEmployeeIDView
from django.urls import path

urlpatterns = [
    path("departaments/<str:departament_id>/projects/<str:project_id>/employees/<pk>/", ProjectEmployeeIDView.as_view()),
    path("departaments/<str:departament_id>/employees/", DepartamentEmployeeView.as_view()),
    path("departaments/<str:departament_id>/employees/<pk>/", DepartamentEmployeeIDView.as_view()),
    path("employees/<pk>/", EmployeeRetrieveUpdateDestroyView.as_view()),
    path("employees/", EmployeeListCreateView.as_view()),
]   
