from rest_framework import serializers
from django.contrib.auth.models import User

##validating the request
class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user