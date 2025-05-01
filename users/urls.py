from django.urls import path
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from users.views import PaymentCreateAPIView, PaymentListAPIView, PaymentRetrieveAPIView, PaymentUpdateAPIView, \
    PaymentDestroyAPIView, UserCreateAPIView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("payments/new/", PaymentCreateAPIView.as_view(), name="payment_new"),
    path("payments/", PaymentListAPIView.as_view(), name="payments_list"),
    path("payments/<int:pk>", PaymentRetrieveAPIView.as_view(), name="payment_detail"),
    path("payments/<int:pk>/update/", PaymentUpdateAPIView.as_view(), name="payment_detail"),
    path("payments/<int:pk>/delete/", PaymentDestroyAPIView.as_view(), name="payment_delete"),
    path("register/", UserCreateAPIView.as_view(), name='register'),
    path("login/", CustomTokenObtainPairView.as_view(), name='login'),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]
