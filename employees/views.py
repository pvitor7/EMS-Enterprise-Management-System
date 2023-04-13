from .models import Employees
from .serializers import EmployeeSerializer, DepartamentEmployeeSerializer, GETDepartamentEmployeeSerializer
from departaments.models import Roles
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from .utils import SerializerByMethodMixin

# Create your views here.
class EmployeeListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


class DepartamentEmployeeView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Roles.objects.all()
    serializer_map = {
        'GET': GETDepartamentEmployeeSerializer,
        'POST': DepartamentEmployeeSerializer
    }
    

class DepartamentEmployeeIDView(SerializerByMethodMixin, generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Roles.objects.all()
    serializer_map = {
        'GET': GETDepartamentEmployeeSerializer,
        'PATCH': DepartamentEmployeeSerializer,
        'DELETE': DepartamentEmployeeSerializer
    }