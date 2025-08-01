from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# from rest_framework_simplejwt.views import TokenObtainPairView

# here we 
urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login-refresh/', TokenRefreshView.as_view(), name='token_obtain_refresh'),
]
