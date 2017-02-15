FROM python:3
MAINTAINER Konpat Preechakul <the.akita.ta@gmail.com>

RUN apt-get update 
RUN apt-get install -y --no-install-recommends openssh-client
RUN apt-get install -y --no-install-recommends rsync

VOLUME ["/workdir"]

WORKDIR /workdir

RUN pip install future
RUN pip install pyyaml
RUN pip install arrow
RUN pip install tabulate
RUN pip install capturer
RUN pip install ptyprocess

