from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firebase_uid', 'email', 'display_name', 'photo_url', 
                 'phone_number', 'created_at', 'updated_at']
        read_only_fields = ['firebase_uid', 'created_at', 'updated_at']