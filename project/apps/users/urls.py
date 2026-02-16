from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.users.views import RegisterAPIView, VerifyEmailAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='user-register'),
    path('auth/login/', LoginAPIView.as_view(), name='user-login'),
    path('auth/verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('auth/logout/', LogoutAPIView.as_view(), name='user-logout'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]