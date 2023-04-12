from .models import Project
from .serializers import ProjectSerializer
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

# Create your views here.
class ProjectListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer