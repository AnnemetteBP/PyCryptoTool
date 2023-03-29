# syntax=docker/dockerfile:1
FROM ubuntu:trusty
RUN mkdir -p /code
WORKDIR /code
RUN cd /code

RUN sudo apt-get -y update
RUN sudo apt-get -y upgrade
RUN sudo apt-get install -y sqlite3 libsqlite3-dev
RUN /usr/bin/sqlite3 /code/app.db

FROM python:3.11.2-alpine
RUN apk add --no-cache gcc musl-dev linux-headers
COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade cython
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./ code/app
EXPOSE 5000
CMD ["uvicorn", "main:app", "--host=0.0.0.0" , "--reload" , "--port", "5000"]