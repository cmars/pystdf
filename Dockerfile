FROM python:3.8.11-slim

COPY . /app
WORKDIR /app

RUN ["chmod", "-R", "+x", "scripts"]
