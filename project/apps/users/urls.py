from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.users.views import RegisterAPIView

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='user-register'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]