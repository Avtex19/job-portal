from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.users.views import RegisterAPIView, VerifyEmailAPIView

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='user-register'),
    path('auth/verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]