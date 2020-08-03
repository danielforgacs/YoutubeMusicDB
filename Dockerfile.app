FROM ubuntu:20.04

WORKDIR /home

COPY Pipfile .
COPY Pipfile.lock .

RUN apt update
RUN apt install -y python3.8
RUN apt install -y pipenv
RUN ln /usr/bin/python3.8 /usr/bin/python
RUN pipenv install --system

COPY app/ app/

ENV PYTHONPATH=/home/

EXPOSE 5000
