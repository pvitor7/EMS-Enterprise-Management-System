from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'cellphone']
        extra_kwargs = {'password': {'write_only': True, 'read_only': False}}        
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)  
    
    def update_password(self, instance, password):
        instance.password = make_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            self.update_password(instance, password)
        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)