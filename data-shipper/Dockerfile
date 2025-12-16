FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl

WORKDIR /app

COPY . /app

RUN pip3 install --upgrade pip && pip3 install requests &&  pip3 install python-dotenv

CMD ["python", "./shipper-app.py"]
