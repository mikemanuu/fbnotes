from django.urls import path
from .views import RegisterView, MeView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='auth-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('users/me/', MeView.as_view(), name='user-me'),
]
