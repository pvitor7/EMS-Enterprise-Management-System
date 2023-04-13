from rest_framework import serializers
from .models import Employees
from departaments.models import Departament, Roles
from django.db import transaction


class EmployeeSerializer(serializers.ModelSerializer):
    departament = serializers.SerializerMethodField();
    class Meta:
        model = Employees
        fields = '__all__'
    
    def get_departament(self, obj):
        departament = Roles.objects.filter(employee=obj).first();
        if departament:
            return departament.departament.title
        else:
            return "Departament not found.";
        

class GETDepartamentEmployeeSerializer(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField();
    class Meta:
        model = Roles
        fields = ['id', 'role', 'employee']
        
    def get_employee(self, obj):
        return Employees.objects.get(id=obj.employee.id).name



class DepartamentEmployeeSerializer(serializers.ModelSerializer):
    employee = serializers.CharField()
    class Meta:
        model = Roles
        fields = ['id', 'role', 'employee']
   

    def validate(self, data):
        departament_id = self.context['view'].kwargs.get('departament_id')
        if not departament_id:
            raise serializers.ValidationError({"detail": "Departament ID is required."})
        employee = Employees.objects.filter(name=data['employee']).first();
        if data['employee'] and not employee:
            raise serializers.ValidationError({"detail": "Employee not found."})
        return super().validate(data)


    def create(self, validated_data):
        departament_id = self.context['view'].kwargs.get('departament_id')
        departament = Departament.objects.filter(id=departament_id).first();
        employee = Employees.objects.filter(name=validated_data['employee']).first();
        emplooye_already_associated = Roles.objects.filter(employee=employee, departament=departament).first();
        if emplooye_already_associated:
            raise serializers.ValidationError({"detail": "Employee already associated with the project."})
        
        with transaction.atomic():
            employee_role = Roles.objects.create(employee=employee, departament=departament, role=validated_data['role']);    
        
        return {"id": employee_role.id, "role": employee_role.role, "employee": employee.name}


    def update(self, instance, validated_data):
        departament_id = self.context['view'].kwargs.get('departament_id')
        employee_id = self.context['view'].kwargs.get('departament_id');
        
        departament = Departament.objects.filter(id=departament_id).first();
        employee = Employees.objects.filter(id=employee_id).first();
        
        emplooye_associated = Roles.objects.filter(employee=employee, departament=departament).first();
        
        if not emplooye_associated:
            raise serializers.ValidationError({"detail": "Employee not associated with the project."});
        instance.role = validated_data.get('role')
        return super().update(instance, validated_data);
    
    
    def delete(self, instance):
        departament_id = self.context['view'].kwargs.get('departament_id')
        employee_id = self.context['view'].kwargs.get('pk');
        
        departament = Departament.objects.filter(id=departament_id).first();
        employee = Employees.objects.filter(id=employee_id).first();
        
        emplooye_associated = Roles.objects.filter(employee=employee, departament=departament).first();
        
        if not emplooye_associated:
            raise serializers.ValidationError({"detail": "Employee not associated with the project."});
        return instance;
    
    
    def to_representation(self, instance):
        instance.employee = Employees.objects.get(id=instance.employee.id)
        return super().to_representation(instance)