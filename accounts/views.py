from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response

# Create your views here.

class RegisterView(generics.CreateAPIView):
    # add the queryset
    queryset = User.objects.all()
    # send the data to the register in the serializer
    serializer_class = RegisterSerializer
    
    # return a response
    def create(self, request, *args, **kwargs):
        # get the data from seri
        serializer = self.get_serializer(data=request.data)
        # check if there is an error, raise an exception
        serializer.is_valid(raise_exception=True)
        # if all good then pass it to the serializer to save it into db
        self.perform_create(serializer)
        
        # retun a resp
        return Response({
            "message": f"User {serializer.data['username']} created!",
            "user": serializer.data
        }, status=status.HTTP_201_CREATED)
        
