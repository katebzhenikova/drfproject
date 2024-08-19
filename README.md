Контейнеризация проекта DRF с использованием Docker
Этот проект представляет собой приложение на Django с использованием Django REST Framework (DRF), 
контейнеризированное с помощью Docker. Оно включает несколько сервисов, таких как Django, PostgreSQL, 
Redis и Celery, каждый из которых работает в своём Docker-контейнере для обеспечения масштабируемости и 
удобства развертывания.

Содержание
-Как начать работу
-Структура проекта
-Сервисы
-Переменные окружения
-Запуск проекта
-Остановка проекта
-Доступ к сервисам


Как начать работу
Предварительные требования
Перед началом работы убедитесь, что на вашем компьютере установлены следующие программы:
Docker
Docker Compose

Структура проекта
Проект структурирован следующим образом:

drfproject/
│
│─ Dockerfile             # Dockerfile для сервиса Django
│─ requirements.txt       # Зависимости Python
│─ ...                    # Другие файлы, связанные с Django
│
├─ docker-compose.yml     # Конфигурация Docker Compose
│
├─ .env                   # Файл с переменными окружения
│
└─ README.md              # Этот файл

Сервисы
В этом проекте используются следующие сервисы, каждый из которых работает в своём контейнере:

Django: Основное веб-приложение.
PostgreSQL: Реляционная база данных.
Redis: Хранилище структур данных в памяти, используемое в качестве брокера сообщений для Celery.
Celery: Асинхронная очередь задач.

Переменные окружения
Проект использует файл .env для управления переменными окружения. 
Этот файл должен находиться в корневой директории проекта.

Запуск проекта
Чтобы запустить проект, выполните следующую команду:

docker-compose up -d
Эта команда соберет образы Docker (если они ещё не собраны) и запустит все сервисы в фоновом режиме.

Остановка проекта
Чтобы остановить проект и удалить контейнеры, выполните команду:

docker-compose down
Эта команда остановит все работающие контейнеры и удалит их.

Доступ к сервисам
Django: После запуска проект будет доступен по адресу http://localhost:8000/.
PostgreSQL: База данных будет доступна через контейнер db.
Redis: Redis будет доступен через контейнер redis.

=================================================
Courses

list: http://localhost:8000/course/

Lessons

list: http://localhost:8000/lessons/

Users

list: http://localhost:8000/users/

Payments

list: http://localhost:8000/payments/

Subscription

http://localhost:8000/subscription/

Есть кастомная команда для создания оплаты users.management.commands.add_payment.py

Загрузка данных:

Фикстуры с данными, порядок загрузки

python3 manage.py loaddata material.json
python3 manage.py loaddata user.json
python3 manage.py loaddata groups.json

Сохранение результатов проверки покрытия тестами.

pip install coverage 
coverage run manage.py test 
coverage report -m > coverage_report.txt

В файле coverage_report.txt сохранены результаты тестов

Задачи в фоновом режиме
send_update_notification """Отправка на почту сообщения об обновлении курса"""
last_login_check """Проверка даты последнего входа пользователя"""

для запуска задач на Windows
pip install redis 
Запустить redis из cmd C:\Redis> redis-server.exe
pip install celery (+ настройки в settings.py, __init__)
pip install eventlet 
pip install django-celery-beat  
celery -A config worker -l INFO -P eventlet
celery -A config beat --scheduler django --loglevel=info

Для запуска через Docker

=========================================================
