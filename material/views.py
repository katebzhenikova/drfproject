from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.decorators import permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from material.paginators import CustomPagination, CustomOffsetPagination
from material.models import Course, Lessons, Subscription
from material.permissions import IsModer, IsOwner, IsUserOwner
from material.serializers import CourseSerializer, LessonsSerializer, CourseCreateSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_permissions(self):

        if self.request.user.groups.filter(name="Модераторы").exists():

            if self.action in ["create", "destroy"]:
                self.permission_classes = (~IsModer,)
            elif self.action in ["update", "retrieve"]:
                self.permission_classes = (IsModer,)
        elif self.action != "create":
            self.permission_classes = (IsOwner,)
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


# class CourseCreateAPIView(generics.CreateAPIView):
#     serializer_class = CourseCreateSerializer
#     permission_classes = [IsAuthenticated, ~IsModer]  # Запрещаем создание курсов модераторам
#
#     def perform_create(self, serializer):
#         new_course = serializer.save()
#         new_course.owner = self.request.user
#         new_course.save()


# class CourseRetrieveAPIView(generics.RetrieveAPIView):
#     serializer_class = CourseSerializer
#     queryset = Lessons.objects.all()
#     permission_classes = [IsAuthenticated, IsModer | IsOwner]  # Модераторы и владельцы могут просматривать
#
#
# class CourseUpdateAPIView(generics.UpdateAPIView):
#     serializer_class = CourseSerializer
#     queryset = Lessons.objects.all()
#
#
# class CourseDestroyAPIView(generics.DestroyAPIView):
#     serializer_class = CourseSerializer
#     queryset = Lessons.objects.all()
#     permission_classes = [IsAuthenticated, IsModer | ~IsOwner]  # Модераторы и владельцы могут редактировать


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




