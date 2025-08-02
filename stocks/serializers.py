from rest_framework import serializers
from .models import Stock

# add the model to teh ser
class StockSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Stock
        fields = '__all__'

        
        