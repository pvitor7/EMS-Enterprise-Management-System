from .models import Departament, Roles
from rest_framework import serializers

class DepartamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departament
        fields = '__all__'
        

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id', 'title', 'departament']
        
