
from .views import DepartamentListCreateView, DepartamentRetrieveUpdateDestroyView
from django.urls import path

urlpatterns = [
    path("", DepartamentListCreateView.as_view(), name="departament-list-create-view"),
    path("<pk>/", DepartamentRetrieveUpdateDestroyView.as_view(), name="departament-retrive-view"),
]   