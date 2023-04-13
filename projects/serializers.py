from rest_framework import serializers
from .models import Project, ProjectsEmployees
from employees.models import Employees
from departaments.models import Departament
from django.db import transaction
from django.shortcuts import get_object_or_404



class ProjectSerializer(serializers.ModelSerializer):
    supervisor = serializers.SerializerMethodField();
    class Meta:
        model = Project
        fields = "__all__"
   
    def get_supervisor(self, obj):
        supervisor_project = ProjectsEmployees.objects.filter(project=obj).first();
        if not supervisor_project:
            raise serializers.ValidationError({"detail": "Supervisor not found."});
        return supervisor_project.employee.name;
   
   
    def validate(self, data):
        http_method = self.context['request'].method
        departament_id = self.context['view'].kwargs.get('departament_id')
        if not departament_id:
            raise serializers.ValidationError({"detail": "Departament ID is required."})
        
        project_departament = Project.objects.filter(title=data['title'], departament_id=departament_id)
        if project_departament.exists() and (http_method == 'POST' or http_method == 'PATCH'):
            raise serializers.ValidationError({"detail": "This title of project already exists in departament."})
        
        elif http_method == 'GET' and not project_departament.exists:
            raise serializers.ValidationError({"detail": "Project not found in departament."})
        
        return data


    # def to_representation(self, instance):
    #     departament_id = self.context['view'].kwargs.get('departament_id')
    #     if str(instance.departament.id) != departament_id:
    #         raise serializers.ValidationError({"detail": "Project not found in departament."})
    #     return super().to_representation(instance)


    def create(self, validated_data):
        supervisor_in_validated_data = self.context['request'].data.get('supervisor');
        if not supervisor_in_validated_data:
            raise serializers.ValidationError({"detail": "Supervisor is required."})
        
        supervisor = Employees.objects.filter(name=supervisor_in_validated_data).first();
        if not supervisor:
            raise serializers.ValidationError({"detail": "Supervisor not found."});
        
        departament_id = self.context['view'].kwargs.get('departament_id')
        departament = Departament.objects.get(id=departament_id)

        with transaction.atomic():
            project = Project.objects.create(**validated_data, departament=departament)
            ProjectsEmployees.objects.create(role="Supervisor", employee=supervisor, project=project);
        
        return project

    

    
    def delete(self, instance):
        departament_id = self.context['view'].kwargs.get('departament_id')
        project_id = self.context['view'].kwargs.get('pk')
        
        project = Project.objects.filter(id=project_id, departament_id=departament_id).first()
        if not project:
            raise serializers.ValidationError({"detail": "Project not found in this departament."})
        
        project.delete()
        return instance
    
    
    def update(self, instance, validated_data):
        #verificando se o Projeto a ser atualizado existe no departamento
        departament_id = self.context['view'].kwargs.get('departament_id')
        project_id = self.context['view'].kwargs.get('pk')
        project = Project.objects.filter(id=project_id, departament_id=departament_id).first()
        if not project:
            raise serializers.ValidationError({"detail": "Project not found in this departament."})
        
        #verificando se o supervisor enviado existe no banco
        new_supervisor = validated_data.get("supervisor");
        supervisor_exist = Employees.objects.filter(name=new_supervisor).first();
        if new_supervisor and not supervisor_exist.exists():
            raise serializers.ValidationError("Supervisor not found.");
        
        #filtrando e salvando tabela pivo
        project_supervisor = ProjectsEmployees.objects.filter(employee=supervisor_exist, project=project, role="Supervisor").first();
        if project_supervisor:
            raise serializers.ValidationError({"detail": "The Supervisor is already in charge of the project."});
        
        with transaction.atomic():
            project_supervisor.employee = supervisor_exist;
            project_supervisor.role = "Supervisor";
            project_supervisor.save()
            
            instance.title = validated_data.get('title', instance.title)
            instance.estimed_hours = validated_data.get('estimed_hours', instance.estimed_hours)
            instance.last_hours = validated_data.get('last_hours', instance.last_hours)
            instance.save()
        return instance
    
