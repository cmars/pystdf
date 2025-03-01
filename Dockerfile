FROM python:3.10.0b2-slim

COPY . /app
WORKDIR /app

RUN ["chmod", "-R", "+x", "scripts"]
