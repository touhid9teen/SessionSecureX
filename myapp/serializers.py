from rest_framework import serializers
from .models import TodoModels
from django.contrib.auth.models import User


# class TodoSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = TodoModels
#         fields = '__all__'

#     def create(self, validate_data):
#         return TodoModels.objects.create(**validate_data)

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoModels
        fields = ['id', 'title', 'discription', 'completed', 'created_at']  # Exclude 'user'

    def create(self, validated_data):
        # Get the request user from the context
        user = self.context['request'].user
        # Add user to validated data
        validated_data['user'] = user
        return super().create(validated_data)

class RegistationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email',''),
            password=validated_data['password']
        )
        return user