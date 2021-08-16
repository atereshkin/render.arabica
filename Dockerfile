# syntax=docker/dockerfile:1
FROM debian:bullseye-slim
RUN apt-get update
RUN apt-get -y install --no-install-recommends inkscape xvfb python3 python3-pip
WORKDIR /app
COPY . .
RUN pip install -r reqs.txt
