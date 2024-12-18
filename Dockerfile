FROM debian:latest

RUN apt-get update && apt-get install python python-pip
RUN pip install flask 

ADD ./* /usr/local/bin/molusque
ENV FLASK_APP=index.py

WORKDIR /usr/local/bin/molusque
RUN flask run -h 0.0.0.0 -p 8080
