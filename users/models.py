from django.db import models
from django.contrib.auth.models import AbstractUser

from config import settings
from material.models import Course, Lessons

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта пользователя')
    phone = models.CharField(max_length=35, verbose_name='телефон пользователя', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар пользователя', **NULLABLE)
    city = models.CharField(max_length=10, verbose_name='город', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    pay_data = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    pay_course = models.ForeignKey(Course, verbose_name='оплаченный курс', **NULLABLE, on_delete=models.SET_NULL)
    pay_lesson = models.ForeignKey(Lessons, verbose_name='оплаченный урок', **NULLABLE, on_delete=models.SET_NULL)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма оплаты')
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет')
    ]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f" {self.user.verbose_name} on {self.pay_data.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

