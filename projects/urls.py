
from .views import ProjectListCreateView, ProjectRetrieveUpdateDestroyView
from django.urls import path

urlpatterns = [
    path("", ProjectListCreateView.as_view(), name="projects-list-create-view"),
    path("<pk>/", ProjectRetrieveUpdateDestroyView.as_view(), name="project-retrive-view"),
]   