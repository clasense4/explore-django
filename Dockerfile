FROM python:3.8.5-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /root/src
COPY ./src/requirements.txt .

RUN pip install -r requirements.txt

COPY . .