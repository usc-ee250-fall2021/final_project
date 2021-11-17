# syntax=docker/dockerfile:1
FROM ubuntu:latest
RUN apt update
RUN apt install -y python3 python3-pip python3-dev
RUN pip3 install flask sklearn
WORKDIR .
COPY . .
EXPOSE 5000
ENTRYPOINT FLASK_APP=predict.py flask run --host=0.0.0.0