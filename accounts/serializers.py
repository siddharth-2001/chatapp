from rest_framework import serializers
import re
from django.contrib.auth import password_validation
from django.core.validators import validate_email

from .models import CustomUser as User

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        if len(data['name']) < 3:
            raise serializers.ValidationError('Name must be longer than 2 characters')
        
        elif len(data['phone']) < 10 or re.search('[a-zA-Z]', data['phone']):
            raise serializers.ValidationError('Enter a valid mobile number')
        
        try:
            password_validation.validate_password(data['password'])
        except Exception as e:
            raise serializers.ValidationError({'password': e.messages})
        
        if 'email' not in data:
            return data

        try:
            validate_email(data['email'])
        except Exception as e:
            raise serializers.ValidationError({'email': e.messages})

        
        return data

    class Meta:
        model = User
        fields = '__all__'