FROM python:3.11.5-alpine

# Запрещает питону создавать файлы с кешом
ENV PYTHONDONTWRITEBYTECODE 1
# Логи не буферезируются
ENV PYTHONUNBUFFERED 1

RUN mkdir /krwz_films

# Устанавливаем зависимости для MariaDB и Pillow
RUN apk --no-cache add mariadb-dev jpeg-dev zlib-dev

# Устанавливаем зависимости для сборки mysqlclient
RUN apk --no-cache add build-base

WORKDIR /krwz_films

COPY . /krwz_films

RUN pip install --root-user-action=ignore --upgrade pip
RUN pip install --root-user-action=ignore --upgrade wheel
RUN pip install --root-user-action=ignore --upgrade setuptools
RUN pip install --root-user-action=ignore -r requirements.txt

RUN python manage.py collectstatic --noinput

RUN adduser --disabled-password --no-create-home krwz_films

USER krwz_films
