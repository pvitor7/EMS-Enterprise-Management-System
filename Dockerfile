FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . /code/

RUN apt-get update && apt-get install -y graphviz
RUN apt-get install -y graphviz-dev

RUN pip install -U pip
RUN pip install -r requirements.txt
