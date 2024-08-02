from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, status
from .tasks import send_update_notification
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from material.paginators import CustomPagination, CustomOffsetPagination
from material.models import Course, Lessons, Subscription
from material.permissions import IsModer, IsOwner
from material.serializers import CourseSerializer, LessonsSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        new_course = serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        updated_course = serializer.save()
        subscribers = Subscription.objects.filter(course=updated_course, is_subscribed=True)
        for subscriber in subscribers:
            print(f'Отправка уведомления для {subscriber.user.email}')
            send_update_notification.delay(subscriber.user.email, updated_course.title)


class LessonsCreateAPIView(CreateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = [IsAuthenticated, IsOwner & ~IsModer]  # Только владельцы могут удалять, не модераторы

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonsListAPIView(generics.ListAPIView):
    serializer_class = LessonsSerializer
    queryset = Lessons.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomOffsetPagination


class LessonsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonsSerializer
    queryset = Lessons.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]  # Модераторы и владельцы могут просматривать


class LessonsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonsSerializer
    queryset = Lessons.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]  # Модераторы и владельцы могут редактировать


class LessonsDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonsSerializer
    queryset = Lessons.objects.all()
    permission_classes = [IsOwner, IsAuthenticated]  # Только владельцы могут удалять, не модераторы


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        subscription, created = Subscription.objects.get_or_create(user=user, course=course)

        if not created:
            subscription.delete()
            message = 'Подписка удалена'
        else:
            message = 'Подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)




