from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    # make it write only so you don't return it in the response
    password = serializers.CharField(write_only=True)
    # get the fields from default user
    class Meta: 
        model = User
        fields = ['username', 'email', 'password']
        
        # and now validate and create it into the db
    
    def create(self, validate_data):
        user = User.objects.create_user(
            username=validate_data['username'],
            email=validate_data['email'],
            password=validate_data['password'] # here we has the password
        )
        return user