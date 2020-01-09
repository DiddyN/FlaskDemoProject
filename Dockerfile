FROM python:3.7

MAINTAINER Dimitrije Nesic "dimitrije.nesic@outlook.com"


RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt update -y
RUN apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools -y
RUN apt-get install redis-server -y
RUN pip install --upgrade pip

ADD ./src/ ./app/src
ADD ./requirements.txt ./app

WORKDIR ./app
RUN pip3 install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:./"
ENV PYTHONIOENCODING="utf-8"

CMD ["python3","./src/app.py"]
