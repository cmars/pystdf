FROM python:3.9.5-slim

COPY . /app
WORKDIR /app

RUN ["chmod", "-R", "+x", "scripts"]
