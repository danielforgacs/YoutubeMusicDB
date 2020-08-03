FROM ubuntu:20.04

RUN apt update
RUN apt install -y python3.8 pipenv
RUN ln /usr/bin/python3.8 /usr/bin/python

WORKDIR /home

COPY Pipfile .
COPY Pipfile.lock .
COPY .env .
COPY app/ app/

RUN pipenv install --system

EXPOSE 5000
