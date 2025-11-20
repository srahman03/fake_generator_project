FROM python:3.12-slim
WORKDIR /app

COPY . /app

RUN pip3 install --upgrade pip
RUN pip3 install -r req_pip.txt

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]
