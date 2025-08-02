from django.urls import path
from . import views
urlpatterns = [
    # list all registered stocks
    path('', views.StockListAPIView.as_view(), name='stock-list'),
    #find the symbol
    path('<int:pk>/', views.StockDetailAPIView.as_view(), name='stock-detail'),

    # fetch a new symbol
    path('fetch-symbol/', views.FetchAPIView.as_view(), name='fetch-by-symbol'),
]