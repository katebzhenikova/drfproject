from django.db import models

NULLABLE = {'null': True, 'blank': True}

class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='photo_course/', verbose_name='превью', **NULLABLE)
    description = models.TextField(max_length=500, verbose_name='описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lessons(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='photo_lessons/', verbose_name='превью', **NULLABLE)
    description = models.TextField(max_length=500, verbose_name='описание')
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    video_url = models.URLField(verbose_name='ссылка на видео', **NULLABLE)


    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

