from rest_framework import serializers
from .models import Employees
from departaments.models import Departament, Roles
from projects.models import ProjectsEmployees, Project
from django.db import transaction
from projects.utils import CalculateTime
from django.forms.models import model_to_dict


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
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['weekly_workload'] = CalculateTime.timedelta_to_str(self, instance.weekly_workload)
        return data
         
    
 
class ProjectEmployeeIDSerializer(serializers.ModelSerializer):
    departament = serializers.SerializerMethodField();
    project = serializers.SerializerMethodField();
    class Meta:
        model = Employees
        fields = ['name', 'weekly_workload', 'driver_license', 'departament', 'project']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['weekly_workload'] = CalculateTime.timedelta_to_str(self, instance.weekly_workload)
        return data
        
    def get_departament(self, obj):
        departament_id = self.context['view'].kwargs.get('departament_id')
        departament = Departament.objects.get(id=departament_id)
        return departament.title
    
    def get_project(self, obj):
        project_id = self.context['view'].kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        return project.title    
    
    def validate(self, data):
        departament_id = self.context['view'].kwargs.get('departament_id')
        if not departament_id:
            raise serializers.ValidationError({'detail': 'Departament required.'})
        project_id = self.context['view'].kwargs.get('project_id')
        if not project_id:
            raise serializers.ValidationError({'detail': 'Project required.'})
        pk = self.context['view'].kwargs.get('pk')
        if not pk:
            raise serializers.ValidationError({'detail': 'User ID required.'})
        
        employee = ProjectsEmployees.objects.filter(project=project_id, employee=pk).first();
        
        project = Project.objects.filter(id=project_id, departament=departament_id).first()
        
        if not project:
            raise serializers.ValidationError({'detail': 'Project not found in departament.'})
        
        if not employee:
            raise serializers.ValidationError({'detail': 'User not found im project.'})
        
        return data
     
    
    
class GETDepartamentEmployeeSerializer(serializers.ModelSerializer):
    departament = serializers.SerializerMethodField();
    employee = serializers.SerializerMethodField();
    class Meta:
        model = Roles
        fields = ['id', 'role', 'employee', 'departament']
    
    def get_employee(self, obj):
        if obj.employee:
            return obj.employee.name
        else:
            return "Employee not found.";

    def get_departament(self, obj):
        return obj.departament.title
        


class DepartamentEmployeeSerializer(serializers.ModelSerializer):
    employee = serializers.CharField()
    departament = serializers.SerializerMethodField();
    class Meta:
        model = Roles
        fields = ['id', 'role', 'employee', 'departament']
        read_only_fields = ['departament']
        
    def get_departament(self, obj):
        departament_id = self.context['view'].kwargs.get('departament_id')
        departament = Departament.objects.get(id=departament_id)
        return departament.title
   
    def validate(self, data):
        departament_id = self.context['view'].kwargs.get('departament_id')
        if not departament_id:
            raise serializers.ValidationError({"detail": "Departament ID is required."})
        return super().validate(data)

    def create(self, validated_data):
        departament_id = self.context['view'].kwargs.get('departament_id')
        departament = Departament.objects.filter(id=departament_id).first();
        employee = Employees.objects.filter(name=validated_data['employee']).first();
        if not employee:
            raise serializers.ValidationError({"detail": "Employee not found."})
        emplooye_already_associated = Roles.objects.filter(employee=employee, departament=departament).first();
        if emplooye_already_associated:
            raise serializers.ValidationError({"detail": "Employee already associated with the project."})
        
        with transaction.atomic():
            employee_role = Roles.objects.create(employee=employee, departament=departament, role=validated_data['role']);    
        
        return {"id": employee_role.id, "role": employee_role.role, "employee": employee.name}


    def update(self, instance, validated_data):
        departament_id = self.context['view'].kwargs.get('departament_id')
        employee_id = self.context['view'].kwargs.get('employee_id');
        
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
        return emplooye_associated;
    

     