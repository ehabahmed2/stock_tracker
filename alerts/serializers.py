from rest_framework import serializers
from .models import Alert

class AlertSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Alert
        fields = '__all__'
        read_only_fields = ['user', 'triggered', 'created_at', 'first_triggered_at']
    