from django.urls import path
from .views import EmailOrUsernameLoginAPIView, RegistrationAPIView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login-hapa/', EmailOrUsernameLoginAPIView.as_view(), name='login'),
]
