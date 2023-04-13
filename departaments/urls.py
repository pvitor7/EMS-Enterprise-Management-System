
from .views import DepartamentListCreateView, DepartamentRetrieveUpdateDestroyView
from django.urls import path

urlpatterns = [
    path("departaments/", DepartamentListCreateView.as_view(), name="departament-list-create-view"),
    path("departaments/<pk>/", DepartamentRetrieveUpdateDestroyView.as_view(), name="departament-retrive-view"),
]   