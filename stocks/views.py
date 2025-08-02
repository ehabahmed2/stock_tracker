from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Stock
from .serializers import StockSerializer
import requests
from decouple import config
from rest_framework import generics
# Create your views here.

# api key
api_key = config('F_API_KEY')

# create the class 
class FetchAPIView(APIView):
    # make sure user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    
    # get the request
    def get(self, request): 
        symbol = request.query_params.get('symbol')
        
        if not symbol:
            return Response({'error': 'Please provide a stock symbol.'}, status=status.HTTP_400_BAD_REQUEST)
        # Check if stock exists in DB
        try:
            stock = Stock.objects.get(symbol__iexact=symbol)
            # get updates from for this stock and return json res

            serializer = StockSerializer(stock)
            return Response(serializer.data)
        
        except Stock.DoesNotExist:
            # if it doesn't then fetch this new stock
            url = f"https://financialmodelingprep.com/api/v3/quote-short/{symbol.upper()}?apikey={api_key}"
            res = requests.get(url)
            data = res.json()
            # if there is stock, get data and create it into our db
            if data:
                price = data[0].get("price")
                stock = Stock.objects.create(
                    symbol=symbol.upper(),
                    company_name=symbol.upper(),  # Placeholder for company name later on
                    last_price=price
                )
                # then pass it to the serializer to return json and the resp
                serializer = StockSerializer(stock)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # if not founded return resp not found
            else:
                return Response({'error': 'Stock not found in external API.'}, status=status.HTTP_404_NOT_FOUND)

# show all stocks
class StockListAPIView(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

class StockDetailAPIView(generics.ListAPIView): 
    pass



