FROM python:3.8.10-slim

COPY . /app
WORKDIR /app

RUN ["chmod", "-R", "+x", "scripts"]
