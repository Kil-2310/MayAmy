FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./diploma-frontend ./diploma-frontend
COPY ./diploma-backend ./diploma-backend

WORKDIR /app/diploma-frontend
RUN python setup.py sdist
RUN pip install --no-cache-dir dist/diploma_frontend-0.6.tar.gz

WORKDIR /app/diploma-backend/shop
RUN python manage.py migrate
RUN python manage.py loaddata all_site_data.json

CMD ["gunicorn", "--chdir", "/app/diploma-backend/shop", "shop.wsgi:application", "--bind", "0.0.0.0:8000"]
