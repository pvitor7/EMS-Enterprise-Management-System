from .models import Departament, Roles
from employees.models import Employees
from rest_framework import serializers


class DepartamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departament
        fields = '__all__'
        

# class RolesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Roles
#         fields = ['id', 'title', 'departament']
        

class DepartamentEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ['name']
        
            
    def validate(self, data):
        departament_id = self.context['view'].kwargs.get('departament_id')
        employee_id = self.context['view'].kwargs.get('pk')
        if not departament_id:
            raise serializers.ValidationError({"detail": "Departament ID is required."})
        if not employee_id:
            raise serializers.ValidationError({"detail": "Employee ID is required."})
        return data
    
    
    def update(self, instance, validated_data):
        departament_id = self.context['view'].kwargs.get('departament_id')
        employee_id = self.context['view'].kwargs.get('pk')
        Roles.objects.filter(employee=employee_id, departament_id=departament_id).update(**validated_data)
        return instance

        
    def delete(self):
        import ipdb ; ipdb.set_trace()
        departament_id = self.context['view'].kwargs.get('departament_id')
        employee_id = self.context['view'].kwargs.get('pk')
        Roles.objects.filter(employee=employee_id, departament_id=departament_id).delete()
        return self
    
    