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


=========================================================
