from django.urls import path
from . import views
urlpatterns = [
    path('', views.ListCreateAPIview.as_view(), name='alert-list-create'),
    path('<int:pk>/', views.AlertActionAPIview.as_view(), name='alert-action'),
]