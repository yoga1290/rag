FROM quay.io/jupyter/base-notebook:ubuntu-24.04

USER root

RUN apt-get update
RUN apt-get install -y gcc build-essential

COPY . .
RUN pip install --upgrade -r requirements.txt