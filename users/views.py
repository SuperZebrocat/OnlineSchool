from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import create_stripe_price, create_stripe_session


class PaymentCreateAPIView(generics.CreateAPIView):
    """Создание платежа."""

    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        user = self.request.user
        payment = serializer.save(user=user)

        if payment.payment_method == Payment.TRANSFER:
            price = create_stripe_price(payment)
            session_id, payment_link = create_stripe_session(price)
            payment.session_id = session_id
            payment.link = payment_link
            payment.save()


class PaymentListAPIView(generics.ListAPIView):
    """Список платежей."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "payment_method")
    ordering_fields = ("payment_date",)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Детали платежа."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentUpdateAPIView(generics.UpdateAPIView):
    """Редактирование платежа."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentDestroyAPIView(generics.DestroyAPIView):
    """Удаление платежа."""

    queryset = Payment.objects.all()


class UserCreateAPIView(generics.CreateAPIView):
    """Регистрация пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        # хэшируем пароль пользователя
        user.set_password(user.password)
        user.save()


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        user = self.get_user_from_token(response.data["access"])
        if user:
            user.last_login = timezone.now()
            user.save(update_fields=["last_login"])

        return response

    def get_user_from_token(self, token):
        decoded_token = AccessToken(token)
        user_id = decoded_token["user_id"]
        return User.objects.get(id=user_id)
