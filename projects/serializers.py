from rest_framework import serializers
from .models import Project, ProjectsEmployees
from employees.models import Employees
from departaments.models import Departament
from django.db import transaction
from .utils import CalculateTime
from datetime import datetime


class ProjectRepresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'last_hours', 'departament', 'estimed_date', 'date_last_estimate_calc','completed_hours', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['last_hours'] = CalculateTime.timedelta_to_str(self, instance.last_hours)
        data['completed_hours'] = CalculateTime.timedelta_to_str(self, instance.completed_hours)
        return data

    

class ProjectSerializer(serializers.ModelSerializer):
    supervisor = serializers.SerializerMethodField();
    last_hours = serializers.CharField();
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'last_hours', 'departament', 'estimed_date', 'date_last_estimate_calc', 'supervisor', 'completed_hours']
        read_only_fields = ['estimed_date', 'date_last_estimate_calc', 'completed_hours']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['last_hours'] = CalculateTime.timedelta_to_str(self, instance.last_hours)
        data['completed_hours'] = CalculateTime.timedelta_to_str(self, instance.completed_hours)
        data['departament'] = instance.departament.title
        return data
        
    def get_supervisor(self, obj):
        supervisor_project = ProjectsEmployees.objects.filter(project=obj, role="Supervisor").first();
        if supervisor_project.employee:
            return supervisor_project.employee.name;
        return "Supervisor not found.";
        
        
    def validate(self, data):
        departament_id = self.context['view'].kwargs.get('departament_id')
        if not departament_id:
            raise serializers.ValidationError({"detail": "Departament ID is required."})
        return data


    def create(self, validated_data):
        departament_id = self.context['view'].kwargs.get('departament_id')
        departament = Departament.objects.get(id=departament_id)
        
        supervisor_in_validated_data = self.context['request'].data.get('supervisor');
        if not supervisor_in_validated_data:
            raise serializers.ValidationError({"detail": "Supervisor is required."})
        
        supervisor = Employees.objects.filter(name=supervisor_in_validated_data).first();
        if not supervisor:
            raise serializers.ValidationError({"detail": "Supervisor not found."});
        estimed_date = CalculateTime.convert_days_hours_minutes(self, validated_data['last_hours']);
        validated_data['estimed_date'] = estimed_date;
        validated_data['date_last_estimate_calc'] = datetime.today().date();

        validated_data['last_hours'] = CalculateTime.str_to_timedelta(self, validated_data['last_hours'])
        
        title = validated_data.get('title');
        project_already_exists = Project.objects.filter(title=title, departament=departament_id)
        
        if project_already_exists:
            raise serializers.ValidationError({"detail": "Project already exist in departament."})

        with transaction.atomic():
            project = Project.objects.create(**validated_data, departament=departament)
            ProjectsEmployees.objects.create(**{"role": "Supervisor", "employee": supervisor, "project": project});
        return project


    def delete(self, instance):
        departament_id = self.context['view'].kwargs.get('departament_id')
        project_id = self.context['view'].kwargs.get('pk')
        if not project_id:
            raise serializers.ValidationError({"detail": "Project ID is required."})
        
        project = Project.objects.filter(id=project_id, departament_id=departament_id).first()
        if not project:
            raise serializers.ValidationError({"detail": "Project not found in this departament."})
        
        project.delete()
        return instance
    
    
    def update(self, instance, validated_data):
        departament_id = self.context['view'].kwargs.get('departament_id')
        project_id = self.context['view'].kwargs.get('pk')
        if not project_id:
            raise serializers.ValidationError({"detail": "Project ID is required."})
        
        project = Project.objects.filter(id=project_id, departament_id=departament_id).first()
        if not project:
            raise serializers.ValidationError({"detail": "Project not found in this departament."})
        
        new_supervisor = self.context['request'].data.get('supervisor');
        supervisor_exist = Employees.objects.filter(name=new_supervisor).first();
        if new_supervisor and not supervisor_exist:
            raise serializers.ValidationError({"detail": "Supervisor not found."});
        
        supervisor_project = ProjectsEmployees.objects.filter(project=project, role="Supervisor").first();
        if supervisor_project:
            supervisor_project.employee = supervisor_exist
            supervisor_project.save()
        else:
            if supervisor_exist:
                ProjectsEmployees.objects.create(project=project, employee=supervisor_exist, role="Supervisor");
        
        if validated_data.get('last_hours'):
            instance.last_hours = CalculateTime.str_to_timedelta(self, validated_data['last_hours'])
            validated_data['last_hours'] = CalculateTime.str_to_timedelta(self, validated_data['last_hours'])
        
        last_hours_recalc = CalculateTime.calculate_hours_project(self, instance)
        validated_data['completed_hours'] = last_hours_recalc
        departament = Departament.objects.filter(id=departament_id).first()
        validated_data['departament'] = departament or instance.departament
        validated_data['estimed_date'] = CalculateTime.convert_days_hours_minutes(self, last_hours_recalc, instance.created_at)
        return super().update(instance, validated_data)



class ProjectEmployeeSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(write_only=True)
    employee_name = serializers.CharField(source='employee.name', read_only=True)

    class Meta:
        model = ProjectsEmployees
        fields = ['id', 'role', 'employee', 'employee_name']
        extra_kwargs = {'employee': {'read_only': False}}
        

    def create(self, validated_data):
        project_id = self.context['view'].kwargs.get('pk')
        project = Project.objects.filter(id=project_id).first();
        if not project:
            raise serializers.ValidationError({"detail": "Project not found."})
        
        employee_name = validated_data.get('employee');
        employee = Employees.objects.filter(name=employee_name).first();
        if not employee:
            raise serializers.ValidationError({"detail": "Employee is required."})
        
        role = validated_data.get('role');
        if not role:
            raise serializers.ValidationError({"detail": "Role is required.."});

        can_participate = CalculateTime.get_next_project(self, project, employee)
        if not can_participate:
            raise serializers.ValidationError({"detail": "The employee is not able to participate in the project for exceeding the allowed weekly hours limit."})
        
        employee_in_project = ProjectsEmployees.objects.filter(employee_id=employee.id, project_id=project.id).first();
        if employee_in_project:
            raise serializers.ValidationError({"detail": "Employee already exist in this project."})

        recalculate_hours = CalculateTime.calculate_hours_project(self, project, employee);
        Project.objects.filter(id=project.id).update(last_hours=recalculate_hours);
                
        validated_data['project'] = project
        validated_data['employee'] = employee
        return super().create(validated_data);      