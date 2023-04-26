from .models import Project, ProjectsEmployees
from .serializers import ProjectSerializer, ProjectEmployeeSerializer, ProjectRepresentationSerializer
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from employees.utils import SerializerByMethodMixin



# Create your views here.
class ProjectListCreateView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_map = {
        'GET': ProjectRepresentationSerializer,
        'POST': ProjectSerializer,
    }
    # serializer_class = ProjectSerializer


class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    
class ProjectsEmployeeListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ProjectsEmployees.objects.all()
    serializer_class = ProjectEmployeeSerializer
    
    
class ProjectEmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ProjectsEmployees.objects.all()
    serializer_class = ProjectEmployeeSerializer
    