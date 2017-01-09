FROM python:3
MAINTAINER Konpat Preechakul <the.akita.ta@gmail.com>

COPY . /tmp
RUN cd tmp \
    && python setup.py install

RUN apt-get update 
RUN apt-get install -y openssh-client
RUN apt-get install -y rsync

CMD rdocker --help
