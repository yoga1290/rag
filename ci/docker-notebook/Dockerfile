FROM quay.io/jupyter/base-notebook:ubuntu-24.04

USER root
RUN apt-get update
RUN apt-get install -y gcc build-essential
USER jovyan

RUN pip install \
    "yoga1290.rag[infrastructure-local-llama-postgres]==0.1.33"