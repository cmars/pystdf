FROM python:3.8.9-slim

COPY . /app
WORKDIR /app

RUN ["chmod", "-R", "+x", "scripts"]
