from .models import Employees
from .serializers import EmployeeSerializer, DepartamentEmployeeSerializer, GETDepartamentEmployeeSerializer,  ProjectEmployeeIDSerializer
from departaments.models import Roles
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .utils import SerializerByMethodMixin

# Create your views here.
class EmployeeListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


class DepartamentEmployeeView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Roles.objects.all()
    serializer_map = {
        'GET': GETDepartamentEmployeeSerializer,
        'POST': DepartamentEmployeeSerializer
    }
    

class DepartamentEmployeeIDView(SerializerByMethodMixin, generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Roles.objects.all()
    serializer_map = {
        'GET': EmployeeSerializer,
        'PATCH': DepartamentEmployeeSerializer,
        'DELETE': DepartamentEmployeeSerializer
    }


class ProjectEmployeeIDView(generics.RetrieveDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Employees.objects.all()
    serializer_class =  ProjectEmployeeIDSerializer
