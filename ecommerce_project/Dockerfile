FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

COPY ./requirements.txt /app/reqirements.txt

RUN pip install -r reqirements.txt

copy . /app