FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./diploma-frontend ./diploma-frontend
COPY ./diploma-backend/shop ./diploma-backend

WORKDIR /app/diploma-frontend
RUN python setup.py sdist
RUN pip install --no-cache-dir dist/diploma_frontend-0.6.tar.gz
