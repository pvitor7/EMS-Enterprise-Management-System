from .models import Departament
from employees.models import Employees
from .serializers import DepartamentSerializer, DepartamentEmployeeSerializer
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class DepartamentListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Departament.objects.all()
    serializer_class = DepartamentSerializer


class DepartamentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Departament.objects.all()
    serializer_class = DepartamentSerializer
    
    
class DepartamentEmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Employees.objects.all()
    serializer_class = DepartamentEmployeeSerializer