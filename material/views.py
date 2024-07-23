from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from material.models import Course, Lessons
from material.permissions import IsModer, IsOwner
from material.serializers import CourseSerializer, LessonsSerializer, CourseCreateSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModer]  # Запрещаем создание курсов модераторам
        elif self.action in ['update', 'partial_update', 'retrieve']:
            self.permission_classes = [IsAuthenticated,
                                       IsModer | IsOwner]  # Модераторы и владельцы могут редактировать и просматривать
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated,
                                       IsOwner & ~IsModer]  # Только владельцы могут удалять, не модераторы
        return super().get_permissions()


class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAuthenticated, ~IsModer]  # Запрещаем создание курсов модераторам

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


class CourseRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    queryset = Lessons.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]  # Модераторы и владельцы могут просматривать


class CourseUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    queryset = Lessons.objects.all()


class CourseDestroyAPIView(generics.DestroyAPIView):
    serializer_class = CourseSerializer
    queryset = Lessons.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]  # Модераторы и владельцы могут редактировать


class LessonsCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonsSerializer
    permission_classes = [IsAuthenticated, IsOwner & ~IsModer]  # Только владельцы могут удалять, не модераторы

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonsListAPIView(generics.ListAPIView):
    serializer_class = LessonsSerializer
    queryset = Lessons.objects.all()
    permission_classes = [IsAuthenticated]


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
    permission_classes = [IsAuthenticated, IsOwner & ~IsModer]  # Только владельцы могут удалять, не модераторы





