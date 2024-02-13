FROM python:3.9-buster

RUN apt-get update && apt-get install -y git curl vim

WORKDIR /app

RUN git clone --depth 1 https://github.com/willianantunes/btcrecover.git

WORKDIR /app/btcrecover

RUN pip install -r requirements-full.txt

RUN python run-all-tests.py -vv
