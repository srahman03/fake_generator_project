FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl

WORKDIR /app

COPY . /app

RUN pip3 install --upgrade pip
RUN pip3 install elasticsearch

CMD ["python", "./shipper-app.py"]
