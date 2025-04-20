from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from lms.models import Course, Lesson, Subscription
from lms.paginators import CustomPagination
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModer, IsOwner, IsNotModer


@method_decorator(name="list", decorator=swagger_auto_schema(operation_description="Список курсов."))
@method_decorator(name="destroy", decorator=swagger_auto_schema(operation_description="Удаление курса."))
@method_decorator(name="create", decorator=swagger_auto_schema(operation_description="Создание курса."))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(operation_description="Детали курса."))
@method_decorator(name="update", decorator=swagger_auto_schema(operation_description="Редактирование курса."))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(operation_description="Редактирование курса."))
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (IsNotModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsNotModer | IsOwner,)
        elif self.action == "list":
            self.permission_classes = (IsModer | IsOwner,)
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    """Создание урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsNotModer)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Список уроков."""

    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Детали урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Редактирование урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаление урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class SubscriptionAPIView(APIView):
    """Установка и удаление подписки на обновления курса."""

    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)

        # Проверяем, существует ли подписка
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            # Удаляем подписку
            subs_item.delete()
            message = "Подписка удалена"
        else:
            # Создаем подписку
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        # Возвращаем ответ в API
        return Response({"message": message})
