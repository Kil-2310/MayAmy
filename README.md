**Проект "Интернет магазин товаров""**

Стек: Python, Django, rest_framework, Redis, S3.

Инструкция для запуска проекта:

* Сборка Frontend:
- cd diploma-frontend
- python setup.py sdist
- pip install dist/diploma_frontend-0.6.tar.gz

* Сборка Backend
- cd diploma-backend
- pip install -r requirements.txt
- cd shop/
- python manage.py loaddata all_site_data.json 
- python manage.py runserver