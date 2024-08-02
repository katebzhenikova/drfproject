from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
import logging

from django.conf import settings

from users.models import User

logger = logging.getLogger(__name__)


@shared_task
def send_update_notification(email, course_title):
    """Отправка на почту сообщения об обновлении курса"""
    subject = f'Обновление курса: {course_title}'
    message = f'Уважаемый пользователь,\n\nКурс "{course_title}" был обновлен. Пожалуйста, проверьте новые материалы.'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])


@shared_task
def last_login_check():
    # Получаем текущую дату
    today = timezone.now().date()

    # Вычисляем дату месяц назад
    one_month_ago = today - timedelta(days=30)

    # Находим всех активных пользователей, которые не заходили более месяца
    users_to_block = User.objects.filter(is_active=True, last_login__lt=one_month_ago)

    # Блокируем таких пользователей
    for user in users_to_block:
        user.is_active = False
        user.save()

    return f"Blocked {users_to_block.count()} users"



