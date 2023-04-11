from .models import Employees
from .serializers import EmployeeSerializer
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

# Create your views here.
class EmployeeListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer