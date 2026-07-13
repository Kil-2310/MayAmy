**Проект "Интернет магазин товаров""**

Стек: Python, Django, rest_framework, Redis, S3.

Инструкция для запуска проекта:

* Сборка Frontend:
- pip install -r requirements.txt
- cd diploma-frontend
- python setup.py sdist
- pip install dist/diploma_frontend-0.6.tar.gz

* Сборка Backend
- cd ../diploma-backend/shop/
- python manage.py migrate
- python manage.py loaddata all_site_data.json 
- python manage.py runserver

После установки всех будет доступен url: http://127.0.0.1:8000/
Swagger находится по адресу: http://127.0.0.1:8000/api/schema/swagger/
