FROM debian:latest

RUN apt-get update && apt-get install -y \
    python3-full python3-pip python3-venv git

ENV FLASK_APP=index.py

WORKDIR /usr/local/bin/

RUN git clone https://github.com/MatthieuCollin/molusque

WORKDIR /usr/local/bin/molusque

RUN python3 -m venv /usr/local/bin/molusque/venv
RUN /usr/local/bin/molusque/venv/bin/pip install flask requests

EXPOSE 8080

CMD ["/usr/local/bin/molusque/venv/bin/flask", "run", "-h", "0.0.0.0", "-p", "8080"]
