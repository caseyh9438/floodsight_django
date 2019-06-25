FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /savfloods

WORKDIR /savfloods

ADD . /savfloods/

RUN pip install -r requirements.txt