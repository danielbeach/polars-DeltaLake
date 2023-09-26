FROM ubuntu:20.04

WORKDIR app
COPY . /app

RUN pip3 install -r requirements.txt