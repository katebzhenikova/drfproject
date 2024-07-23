from django.urls import path
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserCreateAPIView

app_name = UsersConfig.name

urlpatterns = [

    path('payment/', PaymentListAPIView.as_view(), name='payment-list'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),

]


