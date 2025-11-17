FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip curl

WORKDIR /app

COPY . /app

RUN /.venv/bin/pip install --upgrade pip
RUN /.venv/bin/pip install -r req_pip.txt

EXPOSE 8000

CMD ["/.venv/bin/gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]