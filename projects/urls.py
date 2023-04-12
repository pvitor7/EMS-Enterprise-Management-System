
from .views import ProjectListCreateView, ProjectRetrieveUpdateDestroyView
from django.urls import path

urlpatterns = [
    path("departaments/<str:departament_id>/projects/", ProjectListCreateView.as_view(), name="projects-list-create-view"),
    path("departaments/<str:departament_id>/projects/<pk>/", ProjectRetrieveUpdateDestroyView.as_view(), name="project-retrive-view"),
]   