FROM python:3.8.13-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN apt update && apt upgrade -y
RUN apt install -y gcc
RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT python main.py