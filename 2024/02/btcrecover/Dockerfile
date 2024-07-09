FROM python:3.12-bullseye

RUN apt-get update && apt-get install -y git curl vim

WORKDIR /app

RUN git clone --depth 1 https://github.com/willianantunes/btcrecover.git

WORKDIR /app/btcrecover

RUN pip install -r requirements-full.txt

RUN python run-all-tests.py -vv
