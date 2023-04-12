from rest_framework import serializers
from .models import Project
from departaments.models import Departament
from django.db import transaction
from django.forms.models import model_to_dict


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
    
   
    def validate(self, data):
        http_method = self.context['request'].method
        departament_id = self.context['view'].kwargs.get('departament_id')
        if not departament_id:
            raise serializers.ValidationError("Departament ID is required.")
                
        project_departament = Project.objects.filter(title=data['title'], departament_id=departament_id)
        if project_departament.exists() and (http_method == 'POST' or http_method == 'PATCH'):
            raise serializers.ValidationError("This title of project already exists in departament.")
        
        return data


    def create(self, validated_data):
        departament_id = self.context['view'].kwargs.get('departament_id')
        departament = Departament.objects.get(id=departament_id)
        project = Project.objects.create(**validated_data, departament=departament)
        return project

    
    def to_representation(self, instance):
        serialized_data = super().to_representation(instance)
        departament_id = self.context['view'].kwargs.get('departament_id')
        if str(instance.departament.id) != departament_id:
            raise serializers.ValidationError("Project not found in departament.")
        return serialized_data

    
    def delete(self):
        departament_id = self.context['view'].kwargs.get('departament_id')
        project_id = self.context['view'].kwargs.get('pk')
        
        project = Project.objects.filter(id=project_id, departament_id=departament_id).first()
        if not project:
            raise serializers.ValidationError("Project not found in this departament.")
        
        project.delete()
        return project
    
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.estimed_hours = validated_data.get('estimed_hours', instance.estimed_hours)
        instance.last_hours = validated_data.get('last_hours', instance.last_hours)
        instance.save()
        return instance
    
