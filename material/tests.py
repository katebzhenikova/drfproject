from rest_framework.reverse import reverse
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from material.models import Lessons, Course, Subscription
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='user@example.com')
        self.course = Course.objects.create(title='Test Course', description='Test Course description', owner=self.user)
        self.lesson = Lessons.objects.create(title='Test Lesson', course=self.course,
                                             description='Test Course description', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        url = reverse('material:course-list')
        data = {
            "title": "New Course",
            "description": "Description for new course",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_update_course(self):
        url = reverse('material:course-detail', args=(self.course.pk,))
        data = {
            "title": "Updated Course Title",
            "description": "Updated Description"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'Updated Course Title')

    def test_delete_course(self):
        url = reverse('material:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.all().count(), 0)

    def test_retrieve_course(self):
        url = reverse('material:course-detail', args=(self.course.pk,))
        response = self.client.get(url, format='json')
        data = response.json()
        # print(data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.course.title
        )

    def test_list_course(self):
        url = reverse('material:course-list')
        response = self.client.get(url)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.all().count(), 1)


class LessonsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='user@example.com')
        self.course = Course.objects.create(title='Test Course', description='Test Course description', owner=self.user)
        self.lesson = Lessons.objects.create(title='Test Lesson', course=self.course,
                                             description='Test Lesson description', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        url = reverse('material:lessons-create')
        data = {
            "title": "New Lesson",
            "description": "Description for new lesson",
            "course": self.course.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lessons.objects.all().count(), 2)

    def test_update_course(self):
        url = reverse('material:lessons-update', args=(self.lesson.pk,))
        data = {
            "title": "Updated Lesson Title",
            "course": self.course.pk
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'Updated Lesson Title')

    def test_delete_course(self):
        url = reverse('material:lessons-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lessons.objects.all().count(), 0)

    def test_retrieve_course(self):
        url = reverse('material:lessons-get', args=(self.lesson.pk,))
        response = self.client.get(url, format='json')
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.lesson.title
        )

    def test_list_course(self):
        url = reverse('material:lessons-list')
        response = self.client.get(url)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lessons.objects.all().count(), 1)


class SubscriptionViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='user@example.com')
        self.course = Course.objects.create(title='Test Course', description='Test Course description', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_creation(self):
        url = reverse('material:subscription')
        data = {
            'course_id': self.course.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_deletion(self):
        Subscription.objects.create(user=self.user, course=self.course)

        url = reverse('material:subscription')
        data = {
            'course_id': self.course.id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())


