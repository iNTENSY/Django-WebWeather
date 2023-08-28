FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

ADD . /code
ADD .env.docker /code/.env

RUN pip install --upgrade pip
RUN pip install -r requirements.txt