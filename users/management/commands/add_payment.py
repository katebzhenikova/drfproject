from django.core.management import BaseCommand, CommandError

from material.models import Course, Lessons
from users.models import User, Payment


class Command(BaseCommand):
    help = 'Добавление оплаты в БД'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(id=1)
            # course = Course.objects.get(id=1)
            lesson = Lessons.objects.get(id=1)
            payment = Payment.objects.create(
                user=user,
                # pay_course=course,
                pay_lesson=lesson,
                pay_amount=500.00,
                payment_method='cash'
            )
            payment.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully added payment {payment.id}'))
        except Exception as e:
            raise CommandError(f'Error adding payment: {e}')

