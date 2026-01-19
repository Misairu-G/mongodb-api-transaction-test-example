FROM mcr.microsoft.com/devcontainers/python:3.14-bookworm

RUN apt-get update && apt-get install -y \
    iputils-ping \
    net-tools \
    ldap-utils \
    ripgrep

RUN pip install ipython
