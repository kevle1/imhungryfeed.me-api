FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip && \
    apt-get install -y gunicorn

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD ./run.sh