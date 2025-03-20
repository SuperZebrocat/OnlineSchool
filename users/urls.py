from django.urls import path
from users.apps import UsersConfig
from users.views import PaymentCreateAPIView, PaymentListAPIView, PaymentRetrieveAPIView, PaymentUpdateAPIView, \
    PaymentDestroyAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
    path("payments/", PaymentListAPIView.as_view(), name="payments_list"),
    path("payments/<int:pk>", PaymentRetrieveAPIView.as_view(), name="payment_detail"),
    path("payments/<int:pk>/update/", PaymentUpdateAPIView.as_view(), name="payment_detail"),
    path("payments/<int:pk>/delete/", PaymentDestroyAPIView.as_view(), name="payment_delete"),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
