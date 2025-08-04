from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Alert
from .serializers import AlertSerializer

# List all alerts for the user & create new
class ListCreateAPIview(generics.ListCreateAPIView):
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated] # to make sure user is logged 
    
    # list all alerts
    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user)
    
    # create a new alert
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


# Retrieve, update, or delete a specific alert
class AlertActionAPIview(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user)
    
    
    
    
    