from material.apps import MaterialConfig
from rest_framework.routers import DefaultRouter
from django.urls import path

from material.views import CourseViewSet, LessonsCreateAPIView, LessonsListAPIView, LessonsRetrieveAPIView, \
    LessonsUpdateAPIView, LessonsDestroyAPIView, CourseCreateAPIView

app_name = MaterialConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/create/', LessonsCreateAPIView.as_view(), name='lessons-create'),
    path('course/create/', CourseCreateAPIView.as_view(), name='course-create'),
    path('lessons/', LessonsListAPIView.as_view(), name='lessons-list'),
    path('lessons/<int:pk>/', LessonsRetrieveAPIView.as_view(), name='lessons-get'),
    path('lessons/update/<int:pk>/', LessonsUpdateAPIView.as_view(), name='lessons-update'),
    path('lessons/delete/<int:pk>/', LessonsDestroyAPIView.as_view(), name='lessons-delete')

] + router.urls


