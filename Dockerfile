FROM python:3-slim

COPY . /app
WORKDIR /app

RUN ["chmod", "-R", "+x", "scripts"]
