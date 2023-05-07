FROM python:3.9-alpine3.16

COPY req.txt /temp/req.txt

COPY app /app

WORKDIR /app

EXPOSE 8000

RUN apk add postgresql-client build-base postgresql

RUN pip install -r /temp/req.txt

RUN adduser --disabled-password app-user

USER app-user