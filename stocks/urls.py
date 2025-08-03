from django.urls import path
from . import views
urlpatterns = [
    # list all registered stocks
    path('', views.StockListAPIView.as_view(), name='stock-list'),
    # fetch a new symbol
    path('fetch-symbol/', views.FetchAPIView.as_view(), name='fetch-by-symbol'),
]