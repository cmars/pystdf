FROM python:3.10.0b4-slim

COPY . /app
WORKDIR /app

RUN ["chmod", "-R", "+x", "scripts"]
