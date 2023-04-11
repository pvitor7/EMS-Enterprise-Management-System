from .models import Departament
from .serializers import DepartamentSerializer
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

# Create your views here.
class DepartamentListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Departament.objects.all()
    serializer_class = DepartamentSerializer


class DepartamentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Departament.objects.all()
    serializer_class = DepartamentSerializer